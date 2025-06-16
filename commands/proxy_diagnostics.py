# commands/proxy_diagnostics.py

import requests
import time

from colors import Colors
from ui import cyberpunk_header, cyberpunk_footer
from effects import clear_screen, wait_for_key

PROXY_FILE = "working_proxies.txt"

def check_proxy_status():
    """
    Display cyberpunk‑styled diagnostics for the first few proxies
    in your PROXY_FILE.
    """
    clear_screen()
    cyberpunk_header("PROXY DIAGNOSTICS", Colors.BRIGHT_YELLOW)

    try:
        with open(PROXY_FILE, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"\n{Colors.BRIGHT_RED}[ERROR]{Colors.RESET} {Colors.BRIGHT_WHITE}Proxy database '{PROXY_FILE}' not found{Colors.RESET}\n")
        cyberpunk_footer()
        wait_for_key()
        return

    count = len(proxies)
    print(f"\n{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_GREEN}DETECTED{Colors.BRIGHT_BLACK}]{Colors.RESET} "
          f"{Colors.BRIGHT_WHITE}Proxy count: {Colors.BRIGHT_CYAN}{count}{Colors.RESET}\n")

    if not proxies:
        print(f"{Colors.BRIGHT_RED}No proxies to test.{Colors.RESET}\n")
    else:
        to_test = min(3, count)
        print(f"{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_YELLOW}TESTING{Colors.BRIGHT_BLACK}]{Colors.RESET} "
              f"{Colors.BRIGHT_WHITE}Running diagnostics on first {to_test} proxies...{Colors.RESET}\n")

        for idx, proxy in enumerate(proxies[:to_test], start=1):
            print(f"{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_CYAN}{idx:02d}{Colors.BRIGHT_BLACK}]{Colors.RESET} "
                  f"{Colors.BRIGHT_WHITE}Testing: {Colors.BRIGHT_YELLOW}{proxy}{Colors.RESET}")

            # Animated spinner
            spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
            for i, ch in enumerate(spinner):
                print(f"\r      {Colors.BRIGHT_CYAN}{ch}{Colors.RESET} {Colors.BRIGHT_WHITE}Connecting...{Colors.RESET}", end="", flush=True)
                time.sleep(0.1)
                if i > 8:
                    break

            proxy_dict = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }

            try:
                r = requests.get("https://api.mail.tm", proxies=proxy_dict, timeout=5)
                if r.status_code == 200:
                    status_color = Colors.NEON_GREEN
                    status_text = "[ONLINE]"
                else:
                    status_color = Colors.NEON_ORANGE
                    status_text = "[DEGRADED]"
                print(f"\r      {status_color}▓{Colors.RESET} "
                      f"{Colors.BRIGHT_WHITE}Status: {status_color}{status_text}{Colors.RESET} "
                      f"{Colors.BRIGHT_BLACK}Response: {status_color}{r.status_code}{Colors.RESET}")
            except requests.exceptions.Timeout:
                print(f"\r      {Colors.NEON_RED}▓{Colors.RESET} "
                      f"{Colors.BRIGHT_WHITE}Status: {Colors.NEON_RED}[TIMEOUT]{Colors.RESET} "
                      f"{Colors.BRIGHT_BLACK}Connection timed out{Colors.RESET}")
            except requests.exceptions.ConnectionError:
                print(f"\r      {Colors.NEON_RED}▓{Colors.RESET} "
                      f"{Colors.BRIGHT_WHITE}Status: {Colors.NEON_RED}[OFFLINE]{Colors.RESET} "
                      f"{Colors.BRIGHT_BLACK}Connection refused{Colors.RESET}")
            except Exception as e:
                print(f"\r      {Colors.NEON_RED}▓{Colors.RESET} "
                      f"{Colors.BRIGHT_WHITE}Status: {Colors.NEON_RED}[ERROR]{Colors.RESET} "
                      f"{Colors.BRIGHT_BLACK}{str(e)[:30]}...{Colors.RESET}")

            print()

    cyberpunk_footer()
    wait_for_key()
