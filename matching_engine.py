#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
import argparse
from typing import List, Tuple, Optional, Dict, Any

# Import application modules (assumes database.py and modals.py are in same dir or in PYTHONPATH)
try:
    import database
    import modals
except Exception as e:
    print("Failed to import local modules database.py or modals.py:", e)
    print("Make sure matching_engine.py is in same folder as database.py and modals.py")
    raise

try:
    from tabulate import tabulate
except Exception:
    print("Missing dependency 'tabulate'. Install with: pip install tabulate")
    raise

# ----------------------------- Utilities --------------------------------

def parse_latlon(location: str) -> Optional[Dict[str, float]]:
    """
    Parse a location string as 'lat,lon' (e.g., '-1.95,30.06').
    Returns dict {'lat': float, 'lon': float} or None if parsing fails.
    """
    if not location or not isinstance(location, str):
        return None
    parts = [p.strip() for p in location.split(',')]
    if len(parts) != 2:
        return None
    try:
        lat = float(parts[0])
        lon = float(parts[1])
        return {"lat": lat, "lon": lon}
    except ValueError:
        return None

def haversine_km(a: Dict[str, float], b: Dict[str, float]) -> float:
    """Return great-circle distance (km) between two points {'lat','lon'}."""
    lat1, lon1 = math.radians(a["lat"]), math.radians(a["lon"])
    lat2, lon2 = math.radians(b["lat"]), math.radians(b["lon"])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    r = 6371.0
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))

def normalize_skill(s: str) -> str:
    return s.strip().lower()

# --------------------------- Matching Logic ------------------------------

class MatchingEngine:
    def __init__(self, db_module=database):
        self.db = db_module

    def _get_all_workers(self) -> List[Dict[str, Any]]:
        return self.db.fetch_all("SELECT * FROM workers WHERE available=1")

    def _get_all_jobs(self) -> List[Dict[str, Any]]:
        return self.db.fetch_all("SELECT * FROM jobs WHERE status='open'")

    def match_job_to_workers(self, job_row: Dict[str, Any], top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Score available workers for the given job row (dict from DB).
        job_row expected fields: job_id, skill_required, location, max_distance (optional)
        """
        workers = self._get_all_workers()
        scored = []
        job_skills = [normalize_skill(s) for s in str(job_row.get("skill_required", "")).split(',') if s.strip()]

        job_loc = parse_latlon(job_row.get("location", "") or "")
        for w in workers:
            score, reasons = self._score_match(job_skills, job_loc, job_row, w)
            scored.append({
                "worker_id": w["worker_id"],
                "name": w["name"],
                "skills": w["skills"],
                "score": score,
                "reasons": reasons,
                "worker_row": w
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        top = scored[:top_n]
        # persist matches to DB matches table
        for r in top:
            try:
                self.db.execute_query(
                    "INSERT INTO matches (job_id, worker_id, match_score) VALUES (?, ?, ?)",
                    (job_row["job_id"], r["worker_id"], int(round(r["score"] * 100)))
                )
            except Exception:
                # if matches table isn't present or insert fails, ignore gracefully
                pass
        return top

    def match_worker_to_jobs(self, worker_row: Dict[str, Any], top_n: int = 10) -> List[Dict[str, Any]]:
        jobs = self._get_all_jobs()
        scored = []
        worker_skills = [normalize_skill(s) for s in str(worker_row.get("skills", "")).split(',') if s.strip()]
        worker_loc = parse_latlon(worker_row.get("location", "") or "")
        for j in jobs:
            score, reasons = self._score_match(worker_skills, worker_loc, j, worker_row, inverse=True)
            scored.append({
                "job_id": j["job_id"],
                "title": j["title"],
                "skill_required": j["skill_required"],
                "score": score,
                "reasons": reasons,
                "job_row": j
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        top = scored[:top_n]
        for r in top:
            try:
                self.db.execute_query(
                    "INSERT INTO matches (job_id, worker_id, match_score) VALUES (?, ?, ?)",
                    (r["job_id"], worker_row["worker_id"], int(round(r["score"] * 100)))
                )
            except Exception:
                pass
        return top

    def _score_match(self, job_skills: List[str], job_loc: Optional[Dict[str, float]], job_row: Dict[str, Any],
                     worker_row: Dict[str, Any], inverse: bool=False) -> Tuple[float, List[str]]:
        """
        Compute a score 0..1 for job vs worker.
        If inverse=False: job_skills param corresponds to job required skills (list), worker_row contains worker.
        If inverse=True: job_skills param is worker skills and job_row is job.
        """
        reasons = []
        # Extract skill lists appropriately
        if inverse:
            # job_skills are actually worker skills; job_row.skill_required is job requirements
            worker_skills = job_skills
            job_required = [normalize_skill(s) for s in str(job_row.get("skill_required", "")).split(',') if s.strip()]
        else:
            job_required = job_skills
            worker_skills = [normalize_skill(s) for s in str(worker_row.get("skills", "")).split(',') if s.strip()]

        # Skill score
        if not job_required:
            skill_score = 0.5
            reasons.append("no required skills (neutral)")
        else:
            matched = set(job_required) & set(worker_skills)
            skill_score = len(matched) / len(job_required)
            reasons.append(f"skills matched {len(matched)}/{len(job_required)}")

        # Proximity score - only if both have lat,lon
        prox_score = 0.5  # neutral default when no location info
        worker_loc = parse_latlon(worker_row.get("location", "") or "")
        job_loc_parsed = job_loc if job_loc is not None else parse_latlon(job_row.get("location", "") or "")
        if worker_loc and job_loc_parsed:
            try:
                dist = haversine_km(worker_loc, job_loc_parsed)
                reasons.append(f"distance {dist:.1f}km")
                # Use a soft scale: <10km -> 1.0, 10-100 -> linear, >100 -> 0
                if dist <= 10:
                    prox_score = 1.0
                elif dist <= 100:
                    prox_score = 1 - ((dist - 10) / 90)  # 1 down to 0
                else:
                    prox_score = 0.0
                reasons.append(f"proximity_score {prox_score:.2f}")
            except Exception:
                reasons.append("proximity calc failed")
                prox_score = 0.5
        else:
            reasons.append("no latlon (proximity neutral)")

        # Simple metadata bonus from worker rating if present in metadata column (not guaranteed)
        bonus = 0.0
        try:
            # If the workers table had a JSON metadata, the earlier DB doesn't; ignore for now
            pass
        except Exception:
            pass

        # Compose weighted score
        w_skill, w_prox, w_bonus = 0.65, 0.25, 0.10
        score = (skill_score * w_skill) + (prox_score * w_prox) + (bonus * w_bonus)
        score = max(0.0, min(1.0, score))
        reasons.append(f"final_score {score:.3f}")
        return score, reasons

# ------------------------ Display Helpers --------------------------------

def display_job_matches(job_row: Dict[str, Any], matches: List[Dict[str, Any]]):
    headers = ["worker_id", "name", "skills", "score", "reasons"]
    rows = []
    for m in matches:
        rows.append([
            m["worker_id"],
            m.get("name") or "",
            m.get("skills") or "",
            f"{m['score']:.3f}",
            "; ".join(m["reasons"])
        ])
    print("\nMatches for Job: {} - {}\n".format(job_row.get("job_id"), job_row.get("title", job_row.get("skill_required", ""))))
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def display_worker_matches(worker_row: Dict[str, Any], matches: List[Dict[str, Any]]):
    headers = ["job_id", "title", "required_skill", "score", "reasons"]
    rows = []
    for m in matches:
        rows.append([
            m["job_id"],
            m.get("title") or "",
            m.get("skill_required") or "",
            f"{m['score']:.3f}",
            "; ".join(m["reasons"])
        ])
    print("\nMatches for Worker: {} - {}\n".format(worker_row.get("worker_id"), worker_row.get("name", "")))
    print(tabulate(rows, headers=headers, tablefmt="grid"))

# ----------------------------- CLI / Demo --------------------------------

def demo(engine: MatchingEngine):
    # Ensure DB exists and get some entries; if no data, create some demo rows
    engine.db.init_database()

    # Create demo farmer, jobs and workers if not present
    farmers = engine.db.fetch_all("SELECT * FROM farmers")
    if not farmers:
        engine.db.execute_query("INSERT INTO farmers (name, phone, location, email) VALUES (?, ?, ?, ?)",
                                ("Demo Farmer", "+250788000000", "-1.95,30.06", "farmer@example.com"))
    workers = engine.db.fetch_all("SELECT * FROM workers")
    if not workers:
        engine.db.execute_query("INSERT INTO workers (name, phone, location, skills, available) VALUES (?, ?, ?, ?, ?)",
                                ("Alice", "+250788111111", "-1.95,30.06", "React,JavaScript", 1))
        engine.db.execute_query("INSERT INTO workers (name, phone, location, skills, available) VALUES (?, ?, ?, ?, ?)",
                                ("Bob", "+250788222222", "-2.05,30.01", "Excel,Data entry", 1))
        engine.db.execute_query("INSERT INTO workers (name, phone, location, skills, available) VALUES (?, ?, ?, ?, ?)",
                                ("Carlos", "+250788333333", "", "GPS,Surveying", 1))

    jobs = engine.db.fetch_all("SELECT * FROM jobs")
    if not jobs:
        # farmer_id 1 assumed from insertion above
        engine.db.execute_query("INSERT INTO jobs (farmer_id, title, description, skill_required, location, duration, pay_rate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (1, "Front-end dev", "Short React build", "React,JavaScript", "-1.9441,30.0619", "2 days", "$30/day"))
        engine.db.execute_query("INSERT INTO jobs (farmer_id, title, description, skill_required, location, duration, pay_rate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (1, "Data entry", "Record harvest data", "Excel", "-1.95,30.06", "1 day", "$10/day"))

    # Pick first job and first worker for demo matching
    job = engine.db.fetch_all("SELECT * FROM jobs LIMIT 1")[0]
    wlist = engine.db.fetch_all("SELECT * FROM workers LIMIT 5")
    worker = wlist[0]

    job_matches = engine.match_job_to_workers(job, top_n=5)
    display_job_matches(job, job_matches)

    worker_matches = engine.match_worker_to_jobs(worker, top_n=5)
    display_worker_matches(worker, worker_matches)

def show_history():
    # Show last 50 matches saved in DB
    database.init_database()
    rows = database.fetch_all("SELECT m.match_id, m.job_id, m.worker_id, m.match_score, m.match_date, j.title, w.name FROM matches m LEFT JOIN jobs j ON m.job_id=j.job_id LEFT JOIN workers w ON m.worker_id=w.worker_id ORDER BY m.match_date DESC LIMIT 50")
    if not rows:
        print("No match history.")
        return
    print(tabulate([[r["match_id"], r["job_id"], r["worker_id"], r["match_score"], r["match_date"], r["title"], r["name"]] for r in rows],
                   headers=["match_id", "job_id", "worker_id", "score", "date", "job_title", "worker_name"], tablefmt="grid"))

def parse_args(argv: List[str]):
    p = argparse.ArgumentParser(description="Matching engine CLI")
    p.add_argument("--demo", action="store_true", help="Create demo data and show matches")
    p.add_argument("--show-history", action="store_true", help="Show recent match history")
    return p.parse_args(argv)

def main(argv: List[str]):
    args = parse_args(argv)
    engine = MatchingEngine()

    if args.demo:
        demo(engine)
        return

    if args.show_history:
        show_history()
        return

    print("No action specified. Use --demo or --show-history")

if __name__ == "__main__":
    main(sys.argv[1:])
