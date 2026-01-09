import os
import sys
import re
from assets.config import CUMULATIVE_RESULTS_DIR
from utils.colors import C, G, R, Y, X

def initialize_search_environment():
    try:
        os.makedirs(CUMULATIVE_RESULTS_DIR, exist_ok=True)
    except OSError as e:
        print(f"{R}Error creating directory {CUMULATIVE_RESULTS_DIR}: {e} {X}")
        sys.exit(1)

def validate_username(username):
    return re.match(r"^[a-zA-Z0-9._]{1,30}$", username)

def get_user_inputs():
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80

    title = "InstaFinder — Recursive chain searcher"
    box_width = len(title) + 4
    padding = (columns - box_width) // 2

    print("\n" + " " * padding + "+" + "-" * (box_width - 2) + "+")
    print(" " * padding + f"| {Y}{title}{X} |")
    print(" " * padding + "+" + "-" * (box_width - 2) + "+")

    i = 0
    target = None
    while i < 3:
        target_input = input(f"\n{C}Enter the username from where you want to start the search (a.k.a Seed username): {X}").strip()
        if validate_username(target_input):
            target = target_input
            break
        print(f"{R}Invalid format. Usernames contain only letters, numbers, dots, and underscores.{X}")
        i += 1

    if not target:
        print(f"\n{R}Invalid username, exiting...{X}")
        sys.exit(0)

    while True:
        k_input = input(f"{C}Enter keywords related to the target (e.g. Name, Full Name, comma-separated): {X}").strip()
        keywords = [k.strip() for k in k_input.split(',') if k.strip()]
        if keywords:
            break
        print(f"{R}You must provide at least one keyword.{X}")

    confirm_header = "--- Confirm Details ---"
    print(f"\n{Y}" + confirm_header.center(columns) + f"{X}")
    print(f"Seed username :   {C}{target}{X}")
    print(f"Keywords (target): {Y}{', '.join(keywords)}{X}")
    confirm = input("\nStart search? (y/n): ").lower()

    if confirm != 'y':
        print(f"{R}Exiting...{X}")
        sys.exit(0)

    return target, keywords
