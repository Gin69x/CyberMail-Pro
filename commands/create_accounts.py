import requests
import random
import string
import time

from colors import Colors
from effects import matrix_rain_effect, wait_for_key
from ui import cyberpunk_header
from progress import display_cyberpunk_progress_bar

PROXY_FILE = "working_proxies.txt"
MAIL_TM_BASE = "https://api.mail.tm"
ACCOUNTS_FILE = "accounts.txt"

def get_random_proxy():
    """
    Load proxies from PROXY_FILE, shuffle them, and return the first
    one that successfully connects to the mail.tm API.
    """
    with open(PROXY_FILE, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    random.shuffle(proxies)

    for proxy in proxies:
        proxy_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        try:
            r = requests.get(MAIL_TM_BASE, proxies=proxy_dict, timeout=10)
            if r.status_code == 200:
                print(f"{Colors.BRIGHT_GREEN}✅ Working proxy: {Colors.BRIGHT_CYAN}{proxy}{Colors.RESET}")
                return proxy_dict
        except requests.RequestException:
            print(f"{Colors.BRIGHT_RED}❌ Proxy failed: {Colors.BRIGHT_BLACK}{proxy}{Colors.RESET}")
    raise RuntimeError("🚫 No working proxies found.")

def generate_random_email():
    """Construct a pseudo‑random local‑part for an email address."""
    return f"ginmail{random.randint(1000, 9999)}"

def generate_password(length=12):
    """Generate a random alphanumeric password."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

def get_domain(proxy):
    """
    Fetch the first available domain from the mail.tm API.
    """
    r = requests.get(f"{MAIL_TM_BASE}/domains", proxies=proxy, timeout=10)
    r.raise_for_status()
    domains = r.json().get("hydra:member", [])
    if not domains:
        raise RuntimeError("❌ No domains returned by API")
    return domains[0]["domain"]

def create_account(username, password, domain, proxy):
    """
    Call the mail.tm account-creation endpoint. On success, append to ACCOUNTS_FILE.
    """
    email = f"{username}@{domain}"
    payload = {"address": email, "password": password}
    r = requests.post(f"{MAIL_TM_BASE}/accounts", json=payload, proxies=proxy, timeout=15)
    if r.status_code == 201:
        print(
            f"\n{Colors.BRIGHT_GREEN}🎉 Created:{Colors.BRIGHT_CYAN} {email}"
            f"{Colors.RESET} | {Colors.BRIGHT_YELLOW}Pwd:{password}{Colors.RESET}"
        )
        with open(ACCOUNTS_FILE, "a") as f:
            f.write(f"{email} | {password}\n")
        return True
    else:
        raise RuntimeError(f"❌ Creation failed: {r.status_code} {r.text}")

def create_accounts_menu():
    """
    Display the 'ACCOUNT INITIALIZATION PROTOCOL' UI, prompt for count,
    then loop creating accounts with progress and error handling.
    """
    cyberpunk_header("ACCOUNT INITIALIZATION PROTOCOL", Colors.BRIGHT_RED)
    try:
        count_str = input(f"{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_RED}>]{Colors.RESET} "
                          f"{Colors.BRIGHT_WHITE}ENTER TARGET ACCOUNT COUNT{Colors.RESET} "
                          f"{Colors.BRIGHT_RED}►{Colors.RESET} ")
        total = int(count_str)
        if total <= 0:
            print(f"{Colors.BRIGHT_RED}Invalid count; must be > 0{Colors.RESET}")
            wait_for_key()
            return
    except ValueError:
        print(f"{Colors.BRIGHT_RED}ERROR: Numeric input expected{Colors.RESET}")
        wait_for_key()
        return

    print(f"\n{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_RED}INIT]{Colors.RESET} "
          f"{Colors.BRIGHT_WHITE}Target:{Colors.BRIGHT_CYAN} {total}{Colors.BRIGHT_WHITE} accounts{Colors.RESET}")
    matrix_rain_effect(1)

    created = 0
    failed = 0

    while created < total:
        # show progress before each attempt
        display_cyberpunk_progress_bar(created, total)
        print("\n")

        try:
            proxy = get_random_proxy()
            domain = get_domain(proxy)
            username = generate_random_email()
            password = generate_password()
            create_account(username, password, domain, proxy)
            created += 1
            time.sleep(0.5)
        except Exception as e:
            failed += 1
            print(f"\n{Colors.BRIGHT_RED}⚠️  {e}{Colors.RESET}")
            if failed >= 5:
                print(f"\n{Colors.BRIGHT_RED}[CRITICAL] Too many failures; aborting.{Colors.RESET}")
                break

    # final summary
    cyberpunk_header("EXECUTION COMPLETE", Colors.BRIGHT_GREEN)
    print(f"\n   {Colors.BRIGHT_GREEN}[SUCCESS]{Colors.RESET} Accounts generated: {Colors.BRIGHT_WHITE}{created}{Colors.RESET}")
    print(f"   {Colors.BRIGHT_RED}[FAILED]{Colors.RESET} Attempts failed: {Colors.BRIGHT_WHITE}{failed}{Colors.RESET}")
    wait_for_key()