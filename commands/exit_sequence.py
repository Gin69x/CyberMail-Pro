import time
import sys
from effects import clear_screen
from colors import Colors

def cyberpunk_exit_sequence():
    """
    Animated cyberpunk-style exit sequence, then terminate the program.
    """
    clear_screen()

    # Static frame: bordered block
    border = "█" * 60
    inner_border = f"{Colors.NEON_GREEN}{'█' * 2}{Colors.RESET}"
    print(f"\n\n{Colors.BRIGHT_BLACK}{border}{Colors.RESET}")
    print(f"{inner_border}{'':<56}{inner_border}")

    # Centered exit text
    exit_text = "NEURAL LINK DISCONNECTING"
    print(f"{inner_border}{Colors.NEON_CYAN}{exit_text:^56}{Colors.RESET}{inner_border}")
    print(f"{inner_border}{'':<56}{inner_border}")
    print(f"{Colors.BRIGHT_BLACK}{border}{Colors.RESET}\n")

    # Progressive disconnection animation frames
    disconnect_frames = [
        (Colors.NEON_GREEN, "████████████████████████", "100%"),
        (Colors.NEON_YELLOW, "██████████████████████  ", " 92%"),
        (Colors.NEON_YELLOW, "████████████████████    ", " 83%"),
        (Colors.NEON_ORANGE, "██████████████████      ", " 75%"),
        (Colors.NEON_ORANGE, "████████████████        ", " 67%"),
        (Colors.NEON_RED,    "██████████████          ", " 58%"),
        (Colors.NEON_RED,    "████████████            ", " 50%"),
        (Colors.NEON_RED,    "██████████              ", " 42%"),
        (Colors.NEON_RED,    "████████                ", " 33%"),
        (Colors.NEON_RED,    "██████                  ", " 25%"),
        (Colors.NEON_RED,    "████                    ", " 17%"),
        (Colors.NEON_RED,    "██                      ", "  8%"),
        (Colors.BRIGHT_BLACK,"                        ", "  0%"),
    ]

    for color, bar, pct in disconnect_frames:
        line = f"[DISCONNECTING] {bar} {pct}"
        print(f"\r{Colors.BRIGHT_WHITE}{line[:15]}{Colors.RESET} {color}{bar}{Colors.RESET} {Colors.BRIGHT_WHITE}{pct}{Colors.RESET}", end="", flush=True)
        time.sleep(0.2)
    print("\n\n")

    # Final messages
    print(f"{Colors.NEON_CYAN}CONNECTION TERMINATED{Colors.RESET}")
    print(f"{Colors.BRIGHT_BLACK}Goodbye, ghost...{Colors.RESET}\n")

    # Final glitch/shake effect for "SYSTEM SHUTDOWN"
    glitched_text = "SYSTEM SHUTDOWN"
    for _ in range(3):
        print(f"\r{Colors.NEON_RED}{glitched_text}{Colors.RESET}", end="", flush=True)
        time.sleep(0.1)
        print(f"\r{Colors.BRIGHT_BLACK}{glitched_text}{Colors.RESET}", end="", flush=True)
        time.sleep(0.1)
    print()

    sys.exit(0)