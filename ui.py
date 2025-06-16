import time
import random
from datetime import datetime
from colors import Colors, SmoothGradientGreens
from effects import clear_screen, glitch_text

# Rich imports for premium UI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt, Confirm
from rich import box
from rich.padding import Padding
from rich.rule import Rule

# Initialize Rich console
console = Console()

def cyberpunk_separator(length=90, style="═"):
    """
    Return a full-width separator line in bright red.
    """
    return f"{Colors.BRIGHT_RED}{style * length}{Colors.RESET}"

def display_logo():
    """
    Clear the screen and draw the full cyberpunk ASCII art logo,
    complete with glitch and drip effects, centered without a box.
    """
    clear_screen()
    
    # Create animated loading effect
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold cyan]Initializing Cyber Grid..."),
        transient=True,
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.01)
    
    console.clear()
    
    # Enhanced logo with Rich styling
    logo_text = Text()
    logo_lines = [
        "╔════════════════════════════════════════════════════════════════════════════════════════╗",
        "║                                                                                        ║",
        " ║   ▄▀▀█▄▄▄▄  ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀█▀▄   ▄▀▀▀▀▄          ▄▀▀▀▀▄   ▄▀▀█▄▄▄▄  ▄▀▀▄ ▀▄    ║",
        "  ║  ▐  ▄▀   ▐ █  █ ▀  █ ▐ ▄▀ ▀▄ █   █ ▀▄ █    █          █        ▐  ▄▀   ▐ █  █▀▄ █  ║",
        "  ║    █▄▄▄▄▄  ▐  █    █   █▄▄▄█ ▐   █  ▐ ▐    █          █    ▀▄▄   █▄▄▄▄▄  ▐  █  ▀█  ║",
        "  ║    █    ▌    █    █   ▄▀   █     █        █           █     █ █  █    ▌    █   █   ║",
        "  ║   ▄▀▄▄▄▄   ▄▀   ▄▀   █   ▄▀   ▄▀▀▀▀▀▄   ▄▀▄▄▄▄▄▄▀     ▐▀▄▄▄▄▀ ▐ ▄▀▄▄▄▄   ▄▀   █    ║",
        "  ║   █    ▐   █    █    ▐   ▐   █       █  █             ▐         █    ▐   █    ▐    ║",
        "  ║   ▐        ▐    ▐            ▐       ▐  ▐                       ▐        ▐         ║",
        " ║                                                                                      ║",
        "  ║                       ╔═╗ ┌─┐ ┌─┐ ┌─┐ ┬ ┬ ┌┐┌ ┌┬┐                                  ║",
        "  ║                       ╠═╣ │   │   │ │ │ │ │││  │                                   ║",
        "  ║                       ╩ ╩ └─┘ └─┘ └─┘ └─┘ ┘└┘  ┴                                   ║",
        " ║                                                                                      ║",
        " ║              ╔═╗ ┬─┐ ┌─┐ ┌─┐ ┌┬┐ ┌─┐ ┬─┐   ╔═╗  ┬ ┬   ╔═╗  ┬  ┌┐┌                    ║",
        "  ║             ║   ├┬┘ ├┤  ├─┤  │  │ │ ├┬┘   ╠═╩╗ └┬┘   ║ ╦  │  │││                   ║",
        " ║              ╚═╝ ┴└─ └─┘ ┴ ┴  ┴  └─┘ ┴└─   ╚══╝  ┴    ╚═╝  ┴  ┘└┘                    ║",
        "║                                                                                        ║",
        "╚════════════════════════════════════════════════════════════════════════════════════════╝"
    ]
    
    # Create gradient effect for logo
    colors = ["#00ff41", "#00e639", "#00cc31", "#00b329", "#009921", "#008019", "#006611", "#004d09"]
    
    # Print logo centered without any box or panel
    console.print(Align.center(Text("\n".join(logo_lines), style="bold green")))
    
    # Animated drip effect using Rich
    drip_chars = []
    for i in range(90):
        if random.random() < 0.15:
            drip_chars.append(Text("▄", style="bright_green"))
        else:
            drip_chars.append(Text(" "))
    
    drip_line = Text()
    for char in drip_chars:
        drip_line.append(char)
    
    console.print(Align.center(drip_line))
    console.print()
    
    # Premium subtitle with gradient effect
    subtitle = Text()
    subtitle.append("[", style="bright_black")
    subtitle.append("CYBERPUNK", style="bold green blink")
    subtitle.append("]", style="bright_black")
    subtitle.append(" EMAIL ", style="bold white")
    subtitle.append("[", style="bright_black")
    subtitle.append("GENERATOR", style="bold green blink")
    subtitle.append("]", style="bright_black")
    
    console.print(Align.center(subtitle))
    console.print()
    console.print()

def display_main_menu():
    """
    Clear screen, re-draw logo, then print a cyberpunk-styled main menu with Rich enhancements.
    """
    display_logo()
    
    # Get console width dynamically
    console_width = console.width
    
    # Create system status table
    status_table = Table(show_header=False, box=box.ROUNDED, style="cyan", width=37)
    status_table.add_column("", style="bright_white", width=20)
    status_table.add_column("", style="bright_cyan", width=17)
    
    now = datetime.now().strftime("%H:%M:%S")
    status_table.add_row("⚡ STATUS  ", "[bold green]ONLINE")
    status_table.add_row("🕒 TIME    ", f"[bold cyan]{now}")
    status_table.add_row("🔒 SECURITY", "[bold green]ENCRYPTED")
    status_table.add_row("🌐 NETWORK ", "[bold yellow]PROXY ACTIVE")
    
    # Create main menu table
    menu_table = Table(
        title="[bold red]◆ MAIN TERMINAL ◆",
        title_style="bold red",
        box=box.DOUBLE_EDGE,
        style="bright_white",
        show_lines=True,
        width=65
    )
    
    menu_table.add_column("CODE", style="bold cyan", width=8)
    menu_table.add_column("OPERATION", style="bold white", width=30)
    menu_table.add_column("STATUS", style="bold green", width=15)
    menu_table.add_column("ACCESS", style="bold yellow", width=10)
    
    # Menu options with enhanced styling
    options = [
        ("01", "INITIALIZE ACCOUNTS", "READY", "GRANTED"),
        ("02", "ACCESS DATABASE", "STANDBY", "SECURED"),
        ("03", "PROXY DIAGNOSTICS", "ACTIVE", "ENABLED"),
        ("04", "ACCESS NODES", "SYNCED", "AWAIT"),
        ("05", "SYSTEM INFO", "ONLINE", "PUBLIC"),
        ("06", "TERMINATE SESSION", "ARMED", "DANGER"),
    ]
    
    for code, operation, status, access in options:
        access_color = {
            "GRANTED": "bold green",
            "SECURED": "bold blue",
            "ENABLED": "bold yellow",
            "AWAIT": "bold purple",
            "PUBLIC": "bold cyan",
            "DANGER": "bold red"
        }.get(access, "white")
        
        menu_table.add_row(
            f"[bold cyan]{code}[/]",
            f"[bold white]►►[/] {operation}",
            f"[bold green]{status}[/]",
            f"[{access_color}]{access}[/]"
        )
        time.sleep(0.1)  # Smooth menu loading
    
    # Create columns layout with proper padding
    console.print(
        Columns(
            [
                Padding(status_table, (0, 1, 0, 1)),
                Padding(menu_table, (0, 1, 0, 1))
            ],
            expand=True,
            equal=False
        ),
        justify="center"
    )
    print("\n")

    # Add glitch effect separator using full console width
    separator = Text("█" * console_width, style="bold green")
    console.print(separator)
    
    # System information bar
    info_text = Text()
    info_text.append("NEURAL LINK: ", style="bright_black")
    info_text.append("ESTABLISHED", style="bold green")
    info_text.append(" | ", style="bright_black")
    info_text.append("FIREWALL: ", style="bright_black")
    info_text.append("ACTIVE", style="bold red")
    info_text.append(" | ", style="bright_black")
    info_text.append("ENCRYPTION: ", style="bright_black")
    info_text.append("AES-256", style="bold cyan")

    console.print(Align.center(info_text))
    console.print(Text("█" * console_width, style="bold green"))

def cyberpunk_input_prompt(message, color=Colors.BRIGHT_CYAN):
    """
    Prompt the user in a styled bracket-arrow format using Rich.
    """
    # Convert color to Rich style
    rich_color = "bright_cyan"
    if color == Colors.BRIGHT_RED:
        rich_color = "bright_red"
    elif color == Colors.BRIGHT_GREEN:
        rich_color = "bright_green"
    elif color == Colors.BRIGHT_YELLOW:
        rich_color = "bright_yellow"
    
    prompt_text = f"[bright_black][[/][{rich_color}]>[/][bright_black]][/] [bold white]{message}[/] [{rich_color}]►[/]"
    
    return Prompt.ask(prompt_text, console=console)

def cyberpunk_header(title, color=Colors.BRIGHT_RED):
    """
    Print a boxed header with a glitchy border around `title` using Rich panels.
    """
    # Convert color to Rich style
    rich_color = "bright_green"
    if color == Colors.BRIGHT_CYAN:
        rich_color = "bright_cyan"
    elif color == Colors.BRIGHT_GREEN:
        rich_color = "bright_green"
    elif color == Colors.BRIGHT_YELLOW:
        rich_color = "bright_yellow"
    
    # Create animated header
    header_text = Text(title, style=f"bold {rich_color}")
    
    # Add glitch effect
    glitched_title = Text()
    for char in title:
        if random.random() < 0.1:
            glitched_title.append(char, style=f"bold {rich_color} blink")
        else:
            glitched_title.append(char, style=f"bold {rich_color}")
    
    panel = Panel(
        Align.center(glitched_title),
        style=rich_color,
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    )
    
    console.print()
    console.print(panel)

def cyberpunk_footer():
    """
    Print a timestamp+status footer matching the header style using Rich.
    """
    now = datetime.now().strftime("%H:%M:%S")
    
    # Create footer table
    footer_table = Table(show_header=False, box=None, style="bright_black")
    footer_table.add_column("", style="bright_white")
    footer_table.add_column("", style="bright_white")
    footer_table.add_column("", style="bright_white")
    
    footer_table.add_row(
        f"[bright_black][[/][bright_green]TIMESTAMP[/][bright_black]][/] [bold white]{now}[/]",
        " | ",
        f"[bright_black][[/][bright_cyan]STATUS[/][bright_black]][/] [bold green]ACTIVE[/]"
    )
    
    # Get console width dynamically
    console_width = console.width
    
    # Create border using full console width
    border = Text("▓" * console_width, style="bright_black")
    
    console.print()
    console.print(border)
    console.print(Align.center(footer_table))
    console.print(border)
    
    # Add subtle pulse effect
    pulse_text = Text("◆ SYSTEM READY ◆", style="bold green blink")
    console.print(Align.center(pulse_text))

# Additional premium functions for enhanced UX
def show_loading_animation(message="Processing", duration=2):
    """
    Show a premium loading animation with spinner and progress bar.
    """
    with Progress(
        SpinnerColumn(spinner_style="cyan"),
        TextColumn(f"[bold cyan]{message}..."),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=True,
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(duration / 100)

def show_success_message(message):
    """
    Display a success message with premium styling.
    """
    success_panel = Panel(
        Align.center(Text(f"✓ {message}", style="bold green")),
        style="bright_green",
        box=box.ROUNDED,
        title="[bold green]SUCCESS",
        title_align="left"
    )
    console.print(success_panel)

def show_error_message(message):
    """
    Display an error message with premium styling.
    """
    error_panel = Panel(
        Align.center(Text(f"✗ {message}", style="bold red")),
        style="bright_red",
        box=box.ROUNDED,
        title="[bold red]ERROR",
        title_align="left"
    )
    console.print(error_panel)

def show_warning_message(message):
    """
    Display a warning message with premium styling.
    """
    warning_panel = Panel(
        Align.center(Text(f"⚠ {message}", style="bold yellow")),
        style="bright_yellow",
        box=box.ROUNDED,
        title="[bold yellow]WARNING",
        title_align="left"
    )
    console.print(warning_panel)