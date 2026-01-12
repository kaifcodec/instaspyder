import sys
import asyncio
import argparse

from instaspyder.cli.cli_interface import initialize_search_environment, get_user_inputs, configuration_menu
from instaspyder.core.config_manager import check_headers, get_config
from instaspyder.core.state_manager import load_search_state, save_search_state, save_cumulative_results_for_keyword
from instaspyder.core.search_logic import recursive_chain_search_async
from instaspyder.core.instagram_api import init_async_client, close_async_client
from instaspyder.utils.colors import C, G, R, Y, X

current_visited_users = set()
current_all_found_matches = []
initial_seed_username_global = ""
search_keywords_global = []

async def cleanup_on_exit():
    print(f"\n{Y}--- Finalizing search results and state ---{X}")
    if initial_seed_username_global:
        save_search_state(initial_seed_username_global, current_visited_users, current_all_found_matches, keywords=search_keywords_global)
    for kw in search_keywords_global:
        save_cumulative_results_for_keyword(kw, current_all_found_matches)
    await close_async_client()

async def run_search_async(seed=None, keywords=None, depth_arg=None):
    global current_visited_users, current_all_found_matches, initial_seed_username_global, search_keywords_global

    initialize_search_environment()

    if seed is None or keywords is None or depth_arg is None:
        initial_seed_username, search_keywords, depth_arg = get_user_inputs()
    else:
        initial_seed_username = seed
        search_keywords = keywords

    initial_seed_username_global = initial_seed_username
    search_keywords_global = search_keywords

    current_visited_users, current_all_found_matches = load_search_state(initial_seed_username, current_keywords=search_keywords)

    if depth_arg is None:
        config = get_config()
        depth_arg = config.get("max_depth", 2)

    await init_async_client()

    try:
        print(f"\n{G}Starting search from {C}@{initial_seed_username}{G} (Limit: {depth_arg} depths) for keywords: {Y}{', '.join(search_keywords)}{X}")

        await recursive_chain_search_async(
            initial_seed_username,
            search_keywords,
            current_visited_users,
            current_all_found_matches,
            depth=0,
            depth_limit=int(depth_arg)
        )
        print(f"\n{G}Overall search completed successfully.{X}")
    except Exception as e:
        if "Instagram Block" in str(e):
            print(f"\n{R}Search halted by Instagram security. State NOT saved to prevent corruption.{X}")
            initial_seed_username_global = None
        else:
            print(f"\n{R}An unhandled error occurred: {e}{X}")
    finally:
        await cleanup_on_exit()


def main():
    parser = argparse.ArgumentParser(description="InstaSpyder — Recursive chain searcher", add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message")
    parser.add_argument("-s", "--seed", help="Seed username to start search from")
    parser.add_argument("-k", "--keywords", help="Comma-separated keywords")
    parser.add_argument("-d", "--depth", type=int, help="Search depth (overrides config)")
    parser.add_argument("-c", "--config", action="store_true", help="Opens interactive configuration menu")

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    if not check_headers():
        print(f"{R}[!] No valid session found.{X}")
        print(f"{Y}You must provide Instagram headers or Login to use this tool.{X}")
        input(f"\nPress Enter to open Configuration Menu...")
        configuration_menu()

        if not check_headers():
            print(f"{R}Still no headers found. Exiting...{X}")
            sys.exit(1)


    config = get_config()
    default_depth = config.get("max_depth", 2)


    if args.depth is not None and args.depth > 2:
        print(f"\n{R} You are using aggressive depth{X} (i.e. {C}{args.depth}{X}) {R}It may flag you session cookies{X}")
        choice = input(f"\n{Y} Do you want to continue? (y/n): ").lower().strip()

        if choice == "n":
            final_choice = input(f"{C}Do you want to continue with default max depth? (i.e. {G}{default_depth}{X}) (y/n): ").lower().strip()
            if final_choice == "y":
                args.depth = default_depth
            else:
                print(f"{R}Exiting...{X}")
                sys.exit(0)
        elif choice != "y":
            print(f"{R}Exiting...{X}")
            sys.exit(0)

    if args.config:
        configuration_menu()
        sys.exit(0)

    cli_keywords = None
    if args.keywords:
        cli_keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]

    try:
        if args.seed and cli_keywords:
            asyncio.run(run_search_async(seed=args.seed, keywords=cli_keywords, depth_arg=args.depth))
        else:
            asyncio.run(run_search_async(depth_arg=args.depth))
    except KeyboardInterrupt:
        print(f"\n{R}Ctrl+C detected. Exiting gracefully...{X}")
        sys.exit(0)

if __name__ == "__main__":
    main()
