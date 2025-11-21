
import os


def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    
    print("\n" + "=" * 60)
    print(f"  {title.upper()}")
    print("=" * 60 + "\n")


def print_separator():
   
    print("-" * 60)


def pause():
   
    input("\nPress Enter to continue...")


def format_table(data, headers):
    
    if not data:
        return "No data to display."
    col_widths = [len(str(h)) for h in headers]
    
    for row in data:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(item)))
            
    col_widths = [w + 4 for w in col_widths]
    
    output = []
    
    format_string = "".join([f"{{:<{w}}}" for w in col_widths])
    
    header_row = format_string.format(*headers)
    output.append(header_row)
    
    separator = "-" * len(header_row)
    output.append(separator)
    
    for row in data:
        str_row = [str(item) for item in row]
        output.append(format_string.format(*str_row))

    return "\n".join(output)


def print_success(message):
   
    print(f"\n SUCCESS: {message}\n")


def print_error(message):
    
    print(f"\n ERROR: {message}\n")


def print_info(message):
    
    print(f"\n INFO: {message}\n")


def get_input(prompt, input_type=str, allow_empty=False):
    
    while True:
        user_input = input(prompt).strip()
        
        if not user_input:
            if allow_empty:
                return None
            else:
                print_error("Input cannot be empty. Please try again.")
                continue
        
        if input_type == int:
            try:
                return int(user_input)
            except ValueError:
                print_error("Please enter a valid number.")
                continue
        elif input_type == float:
            try:
                return float(user_input)
            except ValueError:
                print_error("Please enter a valid decimal number.")
                continue
        else:
            return user_input


def confirm_action(message):
    
    while True:
        response = input(f"\n{message} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print_error("Please enter 'y' or 'n'.")