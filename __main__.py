import signal
import sys
import asyncio

from cli.cli_interface import initialize_search_environment, get_user_inputs
from core.state_manager import load_search_state, save_search_state, save_cumulative_results_for_keyword
from core.search_logic import recursive_chain_search_async
from core.instagram_api import init_async_client, close_async_client
from assets.config import MAX_DEPTH
from utils.colors import C, G, R, Y, X

current_visited_users = set()
current_all_found_matches = []
initial_target_username_global = ""
search_keywords_global = []

def signal_handler(sig, frame):
    print(f"\n{R}Ctrl+C detected. Saving current state and exiting gracefully...{X}")
    asyncio.create_task(cleanup_on_exit())
    sys.exit(0)

async def cleanup_on_exit():
    print(f"\n{Y}--- Finalizing search results and state ---{X}")
    save_search_state(initial_target_username_global, current_visited_users, current_all_found_matches)
    for kw in search_keywords_global:
        save_cumulative_results_for_keyword(kw, current_all_found_matches)
    await close_async_client()

signal.signal(signal.SIGINT, signal_handler)

async def run_search_async():
    global current_visited_users, current_all_found_matches, initial_target_username_global, search_keywords_global

    initialize_search_environment()
    initial_target_username, search_keywords = get_user_inputs()

    initial_target_username_global = initial_target_username
    search_keywords_global = search_keywords

    current_visited_users, current_all_found_matches = load_search_state(initial_target_username)

    await init_async_client()

    try:
        print(f"\n{G}Starting general search from {C}@{initial_target_username}{G} for keywords: {Y}{', '.join(search_keywords)}{X}...")
        print(f"{G}Search will explore up to {Y}{MAX_DEPTH}{G} level(s) deep into suggested user chains.{X}")

        await recursive_chain_search_async(
            initial_target_username,
            search_keywords,
            current_visited_users,
            current_all_found_matches,
            depth=0
        )
        print(f"\n{G}Overall search completed successfully (or exhausted all accessible paths).{X}")
    except Exception as e:
        print(f"\n{R}An unhandled error occurred during search: {e}{X}")
    finally:
        if not sys.exc_info()[0]:
            await cleanup_on_exit()

if __name__ == "__main__":
    asyncio.run(run_search_async())
