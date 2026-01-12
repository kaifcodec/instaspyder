import os
import sys
import re
import json
import getpass

from instaspyder.utils.colors import C, G, R, Y, X
from instaspyder.core.config_manager import get_config, update_config, save_raw_headers
from instaspyder.core.create_headers import create_headers_json, generate_bearer_token, build_header_dictionary

def initialize_search_environment():
    config = get_config()
    results_dir = config.get("results_dir")
    try:
        os.makedirs(results_dir, exist_ok=True)
    except OSError as e:
        print(f"{R}Error creating directory {results_dir}: {e} {X}")
        sys.exit(1)

def validate_username(username):
    return re.match(r"^[a-zA-Z0-9._]{1,30}$", username)

def get_user_inputs():
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80

    title = "InstaSpyder — Recursive chain searcher"
    box_width = len(title) + 4
    padding = (columns - box_width) // 2

    print("\n" + " " * padding + "+" + "-" * (box_width - 2) + "+")
    print(" " * padding + f"| {Y}{title}{X} |")
    print(" " * padding + "+" + "-" * (box_width - 2) + "+")

    i = 0
    seed = None
    while i < 3:
        seed_input = input(f"\n{C}Enter the username from where you want to start the search (a.k.a Seed username): {X}").strip()
        if validate_username(seed_input):
            seed = seed_input
            break
        print(f"{R}Invalid format. Usernames contain only letters, numbers, dots, and underscores.{X}")
        i += 1

    if not seed:
        print(f"\n{R}Invalid username, exiting...{X}")
        sys.exit(0)

    while True:
        k_input = input(f"{C}Enter keywords related to the seed (e.g. Name, Full Name, comma-separated): {X}").strip()
        keywords = [k.strip() for k in k_input.split(',') if k.strip()]
        if keywords:
            break
        print(f"{R}You must provide at least one keyword.{X}")
    depth_arg = None
    if not depth_arg:
        depth_arg = input(f"{C}Enter the searching depth (e.g. 0,1,2) {G}(recommended is 1){X} : ")
    else:
        print(f"{Y}Using default depth (2)...{X}")

    confirm_header = "--- Confirm Details ---"
    print(f"\n{Y}" + confirm_header.center(columns) + f"{X}")
    print(f"Seed username :   {C}{seed}{X}")
    print(f"Keywords (seed): {Y}{', '.join(keywords)}{X}")
    confirm = input("\nStart search? (y/n): ").lower()

    if confirm != 'y':
        print(f"{R}Exiting...{X}")
        sys.exit(0)

    return seed, keywords, depth_arg

def configuration_menu():
    while True:
        config = get_config()
        print(f"\n{Y}--- InstaSpyder Configuration ---{X}")
        print(f" 1. Update Max Search Depth (Current: {C}{config.get('max_depth')}{X})")
        print(f" 2. Change Results Saving Path (Current: {C}{config.get('results_dir')}{X})")
        print(" 3. Login / Update Headers")
        print(" 4. Paste Raw cookies (session, csrf, mid, ds_user_id)")
        print(" 5. Exit this menu")

        choice = input("\nSelect an option: ")

        if choice == '1':
            new_depth = input("Enter max depth (number): ")
            if new_depth.isdigit():
                update_config("max_depth", int(new_depth))
                print(f"{G}Max depth updated to {new_depth}{X}")
            else:
                print(f"{R}Invalid input. Please enter a number.{X}")

        elif choice == '2':
            new_path = input("Enter new absolute path for results: ").strip()
            if os.path.isabs(new_path) or new_path.startswith("./"):
                update_config("results_dir", new_path)
                os.makedirs(new_path, exist_ok=True)
                print(f"{G}Results path updated to: {new_path}{X}")
            else:
                print(f"{R}Invalid path format.{X}")

        elif choice == '3':
            print(f"\n{Y}--- Instagram Login ---{X}")
            u = input("Username: ")
            p = getpass.getpass("Password: ")
            if create_headers_json(u, p):
                print(f"{G}Login successful!{X}")
            else:
                print(f"{R}Login failed.{X}")


        elif choice == '4':
            print(f"\n{Y}--- Manual Header Configuration ---{X}")
            print("Please enter the following values from your session:")

            sid = input(f"{C}1. Session ID: {X}").strip()
            csr = input(f"{C}2. CSRF Token: {X}").strip()
            mid = input(f"{C}3. Machine ID (mid): {X}").strip()
            uid = input(f"{C}4. User ID (ds_user_id/pk): {X}").strip()

            if all([sid, csr, mid, uid]):
                from instaspyder.core.create_headers import build_header_dictionary
                manual_headers = build_header_dictionary(sid, csr, mid, uid)
                save_raw_headers(manual_headers)
                print(f"\n{G}[+] Headers reconstructed and saved successfully!{X}")
            else:
                print(f"\n{R}[!] All 4 values are required.{X}")



        elif choice == '5':
            break
