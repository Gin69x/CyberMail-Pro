import shutil
from effects import clear_screen, animated_loading, pulse_text, rainbow_text, wait_for_key
from ui import display_logo
from colors import Colors

def cyberpunk_startup():
    """
    Display the initial boot sequence:
      1. Clear screen and show “Initializing…” message with spinner
      2. Show logo
      3. Pulse a welcome banner
      4. Rainbow “Press Any Key” prompt
      5. Wait for user to hit Enter
    """
    # 1) Boot message + loading spinner
    clear_screen()
    print(f"\n{Colors.BRIGHT_CYAN}Initializing Email Account Creator...{Colors.RESET}")
    animated_loading(2, "Starting up")

    # 2) Clear and draw logo
    clear_screen()
    display_logo()

    # 3) Pulsing welcome banner
    print(f"\n{Colors.BRIGHT_YELLOW}{'=' * shutil.get_terminal_size().columns}{Colors.RESET}")
    welcome_text = "WELCOME TO EMAIL ACCOUNT CREATOR"
    pulse_text(f"{welcome_text:^65}", Colors.BRIGHT_MAGENTA, pulses=2, centered=True)
    print(f"{Colors.BRIGHT_YELLOW}{'=' * shutil.get_terminal_size().columns}{Colors.RESET}")

    # 4) Rainbow “press any key” line
    press_key_text = "Press Any Key to Start"
    rainbow_line = rainbow_text(press_key_text)
    
    # Center with proper padding
    visible_length = len(press_key_text)  # Length without color codes
    padding = " " * ((shutil.get_terminal_size().columns - visible_length) // 2)
    
    print()  # Spacer
    print(f"\n{padding}{rainbow_line}\n")
    print(f"{Colors.BRIGHT_YELLOW}{'=' * shutil.get_terminal_size().columns}{Colors.RESET}")
    
    # 5) Wait for Enter
    wait_for_key(centered=True)