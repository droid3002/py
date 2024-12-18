import subprocess
import os
import sys
from colorama import init, Fore
os.system("title pyterm beta 1.0")
# Initialize colorama for cross-platform support
init(autoreset=True)

# Global variable to store the current OS type, defaulting to 'other'
current_os = "other"  # Default to 'other'

# A simple function to change text color for the terminal
def change_font(color_name):
    color_dict = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'black': Fore.BLACK
    }
    return color_dict.get(color_name.lower(), Fore.WHITE)  # Default to white if invalid color

# Function to handle OS-specific commands
def run_command(command):
    global current_os
    
    # Define OS-specific command mappings
    os_commands = {
        'windows': {
            'list': 'dir', 'clear': 'cls', 'echo': 'echo'
        },
        'ubuntu': {
            'list': 'ls', 'clear': 'clear', 'echo': 'echo'
        },
        'debian': {
            'list': 'ls', 'clear': 'clear', 'echo': 'echo', 'install': 'sudo apt install'
        },
        'unix': {
            'list': 'ls', 'clear': 'clear', 'echo': 'echo'
        },
        'other': {
            'list': 'ls', 'clear': 'clear', 'echo': 'echo'
        }
    }

    # Get the OS-specific command for 'list' (equivalent to 'dir' in Windows)
    if current_os in os_commands:
        command_map = os_commands[current_os]
    else:
        command_map = os_commands['other']  # Default to 'other'

    # Check if the command is supported for the current OS
    if command in command_map:
        os_command = command_map[command]
        try:
            # Run the OS-specific command
            result = subprocess.run(os_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(result.stderr)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Command '{command}' is not recognized for {current_os}.")

# Function to handle setting OS type
def set_os(os_type):
    global current_os
    valid_os = ['windows', 'ubuntu', 'debian', 'unix', 'other']
    if os_type.lower() in valid_os:
        current_os = os_type.lower()
        print(f"OS set to {current_os.capitalize()}.")
    else:
        print(f"Invalid OS type. Valid options are: {', '.join(valid_os)}.")

# Main function for the terminal
def main():
    current_font = Fore.WHITE  # Default font color
    print("pyterm beta 1.0")
    print("type 'exit' to quit.")
    
    while True:
        # Get the current working directory
        cwd = os.getcwd()
        
        # Prompt with the current directory and a custom font color
        user_input = input(f"{current_font}{cwd}> ")

        # Check for the OS setting command
        if user_input.startswith(";setos"):
            parts = user_input.split()
            if len(parts) == 2:
                set_os(parts[1])  # Set OS based on user input
            else:
                print("Usage: ;setos <os_type>")

        # Check for a font change command
        elif user_input.startswith(";font"):
            parts = user_input.split()
            if len(parts) == 2:
                color = change_font(parts[1])
                if color != Fore.WHITE:
                    current_font = color
                    print(f"Font color changed to {parts[1]}")
                else:
                    print("Invalid font color, using default.")
            else:
                print("Usage: ;font <color_name>")

        # Exit if the user types 'exit'
        elif user_input.lower() == "exit":
            print("Exiting terminal.")
            break
        
        # Run OS-specific commands
        else:
            run_command(user_input)

if __name__ == "__main__":
    main()
