import time
from colors import Colors
from effects import clear_screen, wait_for_key
from ui import cyberpunk_header

ACCOUNTS_FILE = "accounts.txt"

def view_accounts_menu():
    """
    Display stored accounts in a cyberpunk‑styled table.
    """
    clear_screen()
    cyberpunk_header("DATABASE ACCESS", Colors.BRIGHT_BLUE)

    try:
        with open(ACCOUNTS_FILE, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\n{Colors.BRIGHT_RED}[ERROR]{Colors.RESET} "
              f"{Colors.BRIGHT_WHITE}No account database found ({ACCOUNTS_FILE}){Colors.RESET}\n")
        print(f"{Colors.BRIGHT_YELLOW}[SUGGESTION]{Colors.RESET} "
              f"{Colors.BRIGHT_WHITE}Initialize accounts first{Colors.RESET}\n")
        wait_for_key()
        return

    if not lines:
        print(f"\n{Colors.BRIGHT_YELLOW}[WARNING]{Colors.RESET} "
              f"{Colors.BRIGHT_WHITE}No records to display{Colors.RESET}\n")
        wait_for_key()
        return

    # Header row
    print(f"\n{Colors.BRIGHT_BLACK}{'='*80}{Colors.RESET}")
    print(f"{Colors.BRIGHT_WHITE}{'ID':<4} {'EMAIL':<40} {'PASSWORD':<20} {'STATUS':<10}{Colors.RESET}")
    print(f"{Colors.BRIGHT_BLACK}{'='*80}{Colors.RESET}")

    # Display each record with alternating colors
    for idx, entry in enumerate(lines, start=1):
        try:
            email, password = entry.split(" | ")
        except ValueError:
            email = entry
            password = ""
        if idx % 2 == 0:
            id_col    = Colors.BRIGHT_CYAN
            email_col = Colors.BRIGHT_WHITE
            pass_col  = Colors.BRIGHT_YELLOW
        else:
            id_col    = Colors.BRIGHT_MAGENTA
            email_col = Colors.BRIGHT_GREEN
            pass_col  = Colors.BRIGHT_RED

        status_col = Colors.BRIGHT_GREEN
        status_txt = "[ACTIVE]"

        print(f"{id_col}{idx:<4}{Colors.RESET} "
              f"{email_col}{email:<40}{Colors.RESET} "
              f"{pass_col}{password:<20}{Colors.RESET} "
              f"{status_col}{status_txt}{Colors.RESET}")
        time.sleep(0.02)

    print(f"{Colors.BRIGHT_BLACK}{'='*80}{Colors.RESET}\n")

    wait_for_key()