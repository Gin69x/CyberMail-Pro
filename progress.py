from colors import Colors
import time

def display_cyberpunk_progress_bar(current, total, bar_length=50):
    """
    Display a cyberpunk‑themed progress bar.
    
    Usage:
        for i in range(total):
            display_cyberpunk_progress_bar(i, total)
            # ... do work ...
    """
    if total <= 0:
        raise ValueError("Total must be > 0")
    
    progress = current / total
    filled_length = int(bar_length * progress)
    
    # Build bar segments
    filled_bar = "█" * filled_length
    empty_bar = "░" * (bar_length - filled_length)
    
    # Color & status based on thresholds
    if progress < 0.3:
        color = Colors.NEON_RED
        status = "CRITICAL"
    elif progress < 0.7:
        color = Colors.BRIGHT_YELLOW
        status = "CAUTION"
    else:
        color = Colors.BRIGHT_GREEN
        status = "OPTIMAL"
    
    percent_text = f"{round(progress * 100, 1)}%"
    
    # Assemble and print
    bar_display   = f"{Colors.BRIGHT_BLACK}[{color}{filled_bar}{Colors.BRIGHT_BLACK}{empty_bar}{Colors.BRIGHT_BLACK}]{Colors.RESET}"
    status_display = f"{Colors.BRIGHT_BLACK}[{color}{status}{Colors.BRIGHT_BLACK}]{Colors.RESET}"
    count_display  = f"{Colors.NEON_CYAN}{current}{Colors.RESET}/{Colors.NEON_CYAN}{total}{Colors.RESET}"
    
    print(f"\r{bar_display} {percent_text} {status_display} ({count_display})", end="", flush=True)


def display_simple_progress_bar(current, total, bar_length=40):
    """
    A simpler monochrome progress bar with percentage only.
    """
    if total <= 0:
        raise ValueError("Total must be > 0")
    
    progress = current / total
    filled_length = int(bar_length * progress)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    percent = round(progress * 100, 1)
    print(f"\r[{bar}] {percent}% ({current}/{total})", end="", flush=True)


def animated_countup(target, delay=0.05, prefix="", suffix=""):
    """
    Animate a numeric count‑up from 0 to `target`, useful for final summaries.
    
    Example:
        animated_countup(100, prefix="Generated: ", suffix=" accounts")
    """
    for i in range(target + 1):
        print(f"\r{prefix}{i}{suffix}", end="", flush=True)
        time.sleep(delay)
    print()  # move to next line at completion


def complete_and_reset():
    """
    Move to a new line after a progress bar, to prepare
    for subsequent output.
    """
    print()  # simply break the line