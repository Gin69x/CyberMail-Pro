import time
from ui import cyberpunk_header, cyberpunk_footer
from effects import wait_for_key
from colors import Colors

GITHUB_URL = "https://github.com/Gin69x"

def show_about():
    """
    Display the 'SYSTEM INFO' screen with module list, requirements,
    warnings, and creator credit, then wait for user input.
    """
    # 1) Header
    cyberpunk_header("SYSTEM INFO", Colors.NEON_CYAN)

    # 2) Core system description
    print(f"\n{Colors.BRIGHT_BLACK}[{Colors.NEON_PINK}SYSTEM{Colors.BRIGHT_BLACK}]{Colors.RESET} "
          f"{Colors.BRIGHT_WHITE}Neural Email Generator v3.0{Colors.RESET}")
    time.sleep(0.15)

    print(f"{Colors.BRIGHT_BLACK}[{Colors.NEON_CYAN}TYPE{Colors.BRIGHT_BLACK}]{Colors.RESET} "
          f"{Colors.BRIGHT_WHITE}Automated account synthesis protocol{Colors.RESET}")
    time.sleep(0.1)

    # 3) Modules list
    print(f"\n{Colors.BRIGHT_BLACK}[{Colors.NEON_GREEN}MODULES{Colors.BRIGHT_BLACK}]{Colors.RESET}")
    modules = [
        "Proxy rotation matrix",
        "Batch synthesis engine",
        "Neural progress tracking",
        "Holographic interface",
        "Account management core"
    ]
    for m in modules:
        print(f"  {Colors.NEON_CYAN}▸{Colors.RESET} {Colors.BRIGHT_WHITE}{m}{Colors.RESET}")
        time.sleep(0.08)

    # 4) Requirements
    print(f"\n{Colors.BRIGHT_BLACK}[{Colors.NEON_YELLOW}REQUIREMENTS{Colors.BRIGHT_BLACK}]{Colors.RESET}")
    requirements = [
        "working_proxies.txt database",
        "Active neural link connection"
    ]
    for req in requirements:
        print(f"  {Colors.NEON_ORANGE}●{Colors.RESET} {Colors.BRIGHT_WHITE}{req}{Colors.RESET}")
        time.sleep(0.08)

    # 5) Warnings
    print(f"\n{Colors.BRIGHT_BLACK}[{Colors.NEON_RED}WARNING{Colors.BRIGHT_BLACK}]{Colors.RESET}")
    warnings = [
        "Use with caution – corporate monitoring active",
        "Comply with system protocols and ToS"
    ]
    for w in warnings:
        print(f"  {Colors.NEON_RED}!{Colors.RESET} {Colors.BRIGHT_WHITE}{w}{Colors.RESET}")
        time.sleep(0.08)

    # 6) Creator credit
    print(f"\n{Colors.BRIGHT_BLACK}[{Colors.NEON_PINK}CREATOR{Colors.BRIGHT_BLACK}]{Colors.RESET} "
          f"{Colors.BRIGHT_WHITE}🔗 \033]8;;{GITHUB_URL}\033\\Gin\033]8;;\033\\{Colors.RESET}")
    time.sleep(0.1)

    # 7) Footer and wait
    cyberpunk_footer()
    wait_for_key()