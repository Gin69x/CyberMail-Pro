import sys
import os
from startup import cyberpunk_startup
from ui import display_main_menu, cyberpunk_input_prompt
from commands.create_accounts import create_accounts_menu
from commands.view_accounts import view_accounts_menu
from commands.proxy_diagnostics import check_proxy_status
from commands.show_about import show_about
from commands.exit_sequence import cyberpunk_exit_sequence
from commands.login_accounts import login_email_account_menu

# Map menu selections to command functions
PROTOCOLS = {
    '1': create_accounts_menu,
    '2': view_accounts_menu,
    '3': check_proxy_status,
    '4': login_email_account_menu,
    '5': show_about,
    '6': cyberpunk_exit_sequence,
}

def main():
    """
    Boot the app, then enter the main loop:
      1) Display the menu
      2) Prompt for choice
      3) Dispatch to the matching command
      4) Repeat until exit
    """
    if sys.platform == "win32":
        os.system("")

    try:
        # Initial startup animations and logo
        cyberpunk_startup()

        while True:
            # Show the main menu UI
            display_main_menu()

            print("\n")
            # Get user choice
            choice = cyberpunk_input_prompt("Select protocol (1-5):").strip()

            # Lookup and run the corresponding function
            action = PROTOCOLS.get(choice)
            if action:
                action()
            else:
                # Invalid selection feedback
                print(f"\nInvalid choice: {choice}. Please enter a number between 1 and {len(PROTOCOLS)}.\n")
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        cyberpunk_exit_sequence()
    # except Exception as e:
    #     # Catch-all error handler
    #     print(f"\nUnexpected error: {e}\n")
    #     cyberpunk_exit_sequence()

if __name__ == "__main__":
    main()