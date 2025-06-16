from colors import Colors
from effects import matrix_rain_effect, wait_for_key
from ui import cyberpunk_header, cyberpunk_input_prompt
from progress import display_cyberpunk_progress_bar

import requests
import sys
from datetime import datetime
from rich.table import Table
from rich.console import Console
from rich import box

# Initialize Rich console
console = Console(force_terminal=True, color_system="auto")

BASE_URL = "https://api.mail.tm"
MERCURE_URL = "https://mercure.mail.tm/.well-known/mercure"

def cyberpunk_password_prompt(prompt):
    """Password input with asterisk masking in cyberpunk style with navigation"""
    print(prompt, end='', flush=True)
    password = []
    while True:
        ch = getch()
        
        # Handle Enter key
        if ch == '\r' or ch == '\n':
            print()
            return ''.join(password)
            
        # Handle Ctrl+C
        if ch == '\x03':
            raise KeyboardInterrupt
            
        # Handle Backspace
        if ch == '\x08' or ch == '\x7f':
            if password:
                password.pop()
                # Erase last asterisk
                print('\b \b', end='', flush=True)
            continue
            
        # Handle navigation command
        if ch == '<':
            # Clear the password line
            print("\r" + " " * (len(prompt) + len(password) + 10) + "\r", end='', flush=True)
            return None  # Signal to go back to email input
            
        # Regular character
        password.append(ch)
        print('*', end='', flush=True)
    
    return ''.join(password)

# You'll need to add this helper function
def getch():
    """Get a single character from stdin, cross-platform version"""
    try:
        # For Windows
        import msvcrt
        return msvcrt.getch().decode('utf-8')
    except ImportError:
        # For Unix
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def authenticate_email(email, password):
    """Authenticate with Mail.tm API and return token"""
    try:
        response = requests.post(
            f"{BASE_URL}/token",
            json={"address": email, "password": password}
        )
        response.raise_for_status()
        return response.json().get("token")
    except requests.exceptions.RequestException as e:
        error_msg = e.response.json().get("detail", "Authentication failed") if hasattr(e, 'response') else str(e)
        raise Exception(f"Authentication error: {error_msg}")

def fetch_emails(token):
    """Fetch messages from Mail.tm API with proper error handling"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/messages", headers=headers)
        response.raise_for_status()
        return response.json().get("hydra:member", [])  # Correct key is "hydra:member"
    except requests.exceptions.RequestException as e:
        error_msg = e.response.json().get("detail", "Failed to fetch messages") if hasattr(e, 'response') else str(e)
        raise Exception(f"Fetch error: {error_msg}")

def get_message_details(token, message_id):
    """Get full message details"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/messages/{message_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def display_emails_table(emails):
    """
    Display emails in a simple table format using print() with numbering
    """
    if not emails:
        print(f"\n{Colors.BRIGHT_YELLOW}No messages found{Colors.RESET}")
        return
        
    # Print table header
    print(f"\n{Colors.BRIGHT_CYAN}{'#':<3} {Colors.BRIGHT_CYAN}{'FROM':<22} {Colors.BRIGHT_WHITE}{'SUBJECT':<37} {Colors.BRIGHT_YELLOW}{'DATE':<15} {Colors.BRIGHT_GREEN}STATUS{Colors.RESET}")
    print(f"{Colors.BRIGHT_BLACK}{'-'*90}{Colors.RESET}")
    
    for index, email in enumerate(emails, 1):
        # Extract sender information
        sender = email.get('from', {})
        from_name = sender.get('name', sender.get('address', 'Unknown'))
        if len(from_name) > 22:
            from_name = from_name[:19] + "..."
        
        # Truncate long subjects
        subject = email.get('subject', 'No Subject')
        if len(subject) > 37:
            subject = subject[:34] + "..."
        
        # Format date using 'createdAt'
        date_str = email.get('createdAt', 'Unknown')
        try:
            # Simple string slicing since API returns ISO format
            # Format: "2024-01-15T14:30:00.000Z"
            date_str = date_str[5:10] + " " + date_str[11:16]  # Extract MM-DD HH:MM
        except (ValueError, TypeError):
            date_str = 'Unknown'
        
        # Determine status indicator
        if email.get('seen', False):
            status = f"{Colors.BRIGHT_BLACK}READ{Colors.RESET}"
        else:
            status = f"{Colors.BRIGHT_GREEN}NEW{Colors.RESET}"
        
        # Print each row with number
        print(f"{Colors.BRIGHT_YELLOW}{index:<3}{Colors.RESET} {Colors.BRIGHT_CYAN}{from_name:<22}{Colors.RESET} {Colors.BRIGHT_WHITE}{subject:<37}{Colors.RESET} {Colors.BRIGHT_YELLOW}{date_str:<15}{Colors.RESET} {status}")
    
    print(f"\n{Colors.BRIGHT_BLACK}Showing {len(emails)} messages{Colors.RESET}")

def view_email_details(token, email_id):
    """Display detailed view of a single email"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/messages/{email_id}", headers=headers)
        response.raise_for_status()
        email = response.json()
    except Exception:
        print(f"\n{Colors.BRIGHT_RED}Failed to load email details{Colors.RESET}")
        return
    
    cyberpunk_header("EMAIL DETAILS", Colors.NEON_PURPLE)
    
    # Sender information
    sender = email.get('from', {})
    print(f"{Colors.BRIGHT_CYAN}From:{Colors.RESET} {sender.get('name', '')} <{sender.get('address', '')}>")
    
    # Recipients
    to_recipients = [r.get('address', '') for r in email.get('to', [])]
    print(f"{Colors.BRIGHT_CYAN}To:{Colors.RESET} {', '.join(to_recipients)}")
    
    # Date - using 'createdAt'
    date_str = email.get('createdAt', 'Unknown')
    try:
        if 'T' in date_str:
            # Format: "2024-01-15T14:30:00.000Z" -> "2024-01-15 14:30:00"
            date_str = date_str.replace('T', ' ')[:19]
    except:
        pass
    print(f"{Colors.BRIGHT_CYAN}Date:{Colors.RESET} {date_str}")
    
    # Subject
    print(f"{Colors.BRIGHT_CYAN}Subject:{Colors.RESET} {email.get('subject', 'No Subject')}")
    
    # Body
    body = email.get('text', 'No message content')
    if not body:
        body = "No message content"
    print(f"\n{Colors.BRIGHT_WHITE}{body}{Colors.RESET}")
    
    # Attachments
    if email.get('hasAttachments', False):
        attachments = email.get('attachments', [])
        print(f"\n{Colors.BRIGHT_YELLOW}Attachments ({len(attachments)}):{Colors.RESET}")
        for att in attachments:
            print(f"  - {att.get('filename', 'Unnamed')} ({att.get('size', 0)} bytes)")

def login_email_account_menu():
    """
    Display the 'EMAIL ACCOUNT LOGIN' UI with enhanced navigation
    """
    while True:  # Main loop for navigation
        cyberpunk_header("EMAIL ACCOUNT LOGIN", Colors.BRIGHT_BLUE)
        
        # Get email with back option
        email = cyberpunk_input_prompt("ENTER EMAIL ADDRESS (or '<' to go back)", Colors.BRIGHT_CYAN)
        if email.strip() == '<':
            return  # Go back to main menu
            
        # Get password with back option
        password = cyberpunk_password_prompt(
            f"{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_BLUE}>]{Colors.RESET} "
            f"{Colors.BRIGHT_WHITE}ENTER PASSWORD (or '<' to go back){Colors.RESET} "
            f"{Colors.BRIGHT_BLUE}►{Colors.RESET} "
        )
        
        # If user entered '<' in password, restart the loop
        if password is None:
            continue
            
        # Authentication
        print(f"\n{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_BLUE}AUTH]{Colors.RESET} "
              f"{Colors.BRIGHT_WHITE}Authenticating...{Colors.RESET}")
        
        try:
            # Authenticate with Mail.tm
            token = authenticate_email(email, password)
            if not token:
                raise Exception("Authentication failed")
                
            # Fetch emails
            print(f"{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_BLUE}FETCH]{Colors.RESET} "
                  f"{Colors.BRIGHT_WHITE}Retrieving messages...{Colors.RESET}")
            emails = fetch_emails(token)
            
            # Display results
            cyberpunk_header("INBOX ACCESS GRANTED", Colors.BRIGHT_GREEN)
            display_emails_table(emails)
            
            # Inbox action menu
            while True:
                print(f"\n{Colors.BRIGHT_CYAN}INBOX OPTIONS:{Colors.RESET}")
                print(f"  {Colors.BRIGHT_GREEN}[R]{Colors.RESET} Refresh inbox")
                print(f"  {Colors.BRIGHT_GREEN}[B]{Colors.RESET} Back to login")
                print(f"  {Colors.BRIGHT_GREEN}[M]{Colors.RESET} Main menu")
                print(f"\n{Colors.BRIGHT_YELLOW}Or enter a message number to view it{Colors.RESET}")
                
                action = cyberpunk_input_prompt("SELECT ACTION", Colors.BRIGHT_YELLOW).strip().upper()
                
                # Handle message number input
                if action.isdigit():
                    msg_index = int(action) - 1
                    if 0 <= msg_index < len(emails):
                        view_email_details(token, emails[msg_index]['id'])
                        cyberpunk_header("INBOX ACCESS GRANTED", Colors.BRIGHT_GREEN)
                        display_emails_table(emails)
                    else:
                        print(f"{Colors.BRIGHT_RED}Invalid message number. Please enter a number between 1 and {len(emails)}{Colors.RESET}")
                
                # Handle letter commands
                elif action == 'R':
                    # Refresh inbox
                    print(f"{Colors.BRIGHT_BLACK}[{Colors.BRIGHT_BLUE}FETCH]{Colors.RESET} Refreshing messages...")
                    emails = fetch_emails(token)
                    cyberpunk_header("INBOX ACCESS GRANTED", Colors.BRIGHT_GREEN)
                    display_emails_table(emails)
                
                elif action == 'B':
                    # Back to login screen
                    break
                
                elif action == 'M':
                    # Return to main menu
                    return
                
                else:
                    print(f"{Colors.BRIGHT_RED}Invalid option. Please choose R, B, M, or enter a message number.{Colors.RESET}")
            
        except Exception as e:
            cyberpunk_header("ACCESS DENIED", Colors.BRIGHT_RED)
            print(f"\n{Colors.BRIGHT_RED}ERROR: {str(e)}{Colors.RESET}")
            print(f"{Colors.BRIGHT_YELLOW}Check credentials and try again{Colors.RESET}")
            wait_for_key()