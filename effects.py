import time
import random
import threading
import os
import shutil
from colors import Colors

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_effect(text, delay=0.03):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def rainbow_text(text):
    """Return text colored in a repeating rainbow pattern."""
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
    result = ""
    for i, char in enumerate(text):
        if char != " ":
            result += colors[i % len(colors)] + char
        else:
            result += char
    return result + Colors.RESET

def glow_effect(text, color=Colors.CYAN):
    """Wrap text in a glowing bullet-style effect."""
    return f"{color}{Colors.BOLD}✦ {text} ✦{Colors.RESET}"

def animated_loading(duration=2, message="Loading"):
    """
    Show a spinning loader for `duration` seconds.
    e.g. ⠋ Loading... ⠙ Loading... ✓ Loading complete!
    """
    spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    while time.time() < end_time:
        for ch in spinner:
            print(f"\r{Colors.CYAN}{ch} {message}...{Colors.RESET}", end='', flush=True)
            time.sleep(0.1)
            if time.time() >= end_time:
                break
    print(f"\r{Colors.GREEN}✓ {message} complete!{Colors.RESET}" + " " * 10)

def pulse_text(text, color=Colors.BRIGHT_MAGENTA, pulses=3, centered=False):
    """Make text 'pulse' between bold and dim states with optional centering."""
    # Get terminal width for centering
    try:
        import shutil
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80  # Fallback if we can't get terminal size
    
    # Calculate padding if centered
    if centered:
        padding = " " * ((terminal_width - len(text)) // 2)
    else:
        padding = ""
    
    # Pulsing effect with proper padding
    for _ in range(pulses):
        # Bold state
        print(f"\r{padding}{color}{Colors.BOLD}{text}{Colors.RESET}", end='', flush=True)
        time.sleep(0.3)
        # Dim state
        print(f"\r{padding}{Colors.DIM}{text}{Colors.RESET}", end='', flush=True)
        time.sleep(0.3)
    
    # Final bold state
    print(f"\r{padding}{color}{Colors.BOLD}{text}{Colors.RESET}")

def glitch_text(text, intensity=0.1):
    """
    Introduce random glitch characters into `text`.
    intensity=0.1 means ~10% of chars get replaced by █▓▒░▄▀■□▪▫ in red.
    """
    glitch_chars = "█▓▒░▄▀■□▪▫"
    result = ""
    for ch in text:
        if ch != " " and random.random() < intensity:
            result += f"{Colors.BRIGHT_RED}{random.choice(glitch_chars)}{Colors.RESET}"
        else:
            result += ch
    return result

def matrix_rain_effect(duration=1, width=90):
    """
    Quick 'Matrix'-style rain for `duration` seconds.
    Prints random 0/1/blocks columns that scroll once.
    """
    chars = "01█▓▒░"
    iterations = int(duration * 10)
    for _ in range(iterations):
        line = "".join(
            random.choice(chars) if random.random() < 0.1 else " "
            for _ in range(width)
        )
        # randomly color some drops green or white
        colored = "".join(
            f"{random.choice([Colors.GREEN, Colors.BRIGHT_GREEN, Colors.BRIGHT_WHITE])}{c}{Colors.RESET}"
            if c != " " and random.random() < 0.3 else c
            for c in line
        )
        print(f"\r{colored}", end='', flush=True)
        time.sleep(0.1)
    print("\r" + " " * width + "\r", end='', flush=True)

def wait_for_key(prompt="Press Enter to continue", centered=False):
    """
    Display a small spinner and wait for the user to hit Enter, with optional centering.
    Works cross-platform.
    """
    try:
        term_width = shutil.get_terminal_size().columns
    except:
        term_width = 80
    
    # Calculate padding if centered
    if centered:
        # Visible length without color codes
        visible_length = len(prompt) + 2  # +2 for spinner and space
        padding = " " * max(0, (term_width - visible_length) // 2)
    else:
        padding = ""
    
    spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    stop_flag = False

    def animate():
        i = 0
        while not stop_flag:
            ch = spinner[i % len(spinner)]
            # Apply padding for centering
            print(f"\r{padding}{Colors.BRIGHT_CYAN}{ch}{Colors.RESET} {prompt}", end='', flush=True)
            time.sleep(0.1)
            i += 1

    thread = threading.Thread(target=animate, daemon=True)
    thread.start()
    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        stop_flag = True
        # Clear the entire line
        print("\r" + " " * term_width + "\r", end='', flush=True)