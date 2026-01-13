import json
import os
from instaspyder.core.config_manager import get_config, USER_HOME
from instaspyder.utils.colors import C, G, R, Y, X


CACHE_DIR = os.path.join(USER_HOME, ".cache")

def _get_state_filepath(username):
    safe_username = "".join(c for c in username if c.isalnum())
    return os.path.join(USER_HOME, f"search_state_{safe_username}.json")

def silent_cache_metadata(seed_username, users_list):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"metadata_{seed_username}.json")


    new_cleaned_entries = []
    for user in users_list:
        new_cleaned_entries.append({
            "pk": user.get("pk") or user.get("id"),
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "profile_pic_url": user.get("profile_pic_url"),
            "hd_pic_url": user.get("hd_profile_pic_url_info", {}).get("url") # Added for better face rec if available
        })

    try:
        existing_data = []
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []

        # Merge data and avoid duplicates based on user ID (pk)
        existing_pks = {str(u.get('pk')) for u in existing_data if u.get('pk')}

        updated_data = existing_data.copy()
        added_any = False

        for entry in new_cleaned_entries:
            pk_str = str(entry.get('pk'))
            if pk_str not in existing_pks:
                updated_data.append(entry)
                existing_pks.add(pk_str)
                added_any = True

        if added_any or not os.path.exists(cache_file):
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, indent=2, ensure_ascii=False)

    except Exception:
        # Fails silently to ensure the main search logic is never interrupted
        pass

def load_search_state(initial_username, current_keywords=None):
    visited_users = set()
    all_found_matches = []
    state_filepath = _get_state_filepath(initial_username)

    try:
        with open(state_filepath, "r", encoding="utf-8") as f:
            state = json.load(f)
            if state.get("initial_username") == initial_username:
                saved_keywords = state.get("keywords", [])
                if current_keywords and set(current_keywords) != set(saved_keywords):
                    print(f"{Y}[!] Keywords changed. Ignoring previous visited history.{X}")
                    return set(), state.get("found_matches", [])

                visited_users = set(state.get("visited", []))
                all_found_matches = state.get("found_matches", [])
                print(f"{G}[+] Loaded state for '{initial_username}'. Resuming...{X}")
            else:
                print(f"{Y}[!] State mismatch. Starting fresh.{X}")

    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"{R}[-] Error loading state: {e}. Starting fresh.{X}")

    return visited_users, all_found_matches

def save_search_state(initial_username, visited_users, all_found_matches, keywords=None):
    state_filepath = _get_state_filepath(initial_username)
    state = {
        "visited": list(visited_users),
        "found_matches": all_found_matches,
        "initial_username": initial_username,
        "keywords": keywords
    }
    try:
        with open(state_filepath, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"{R}[-] Error saving state: {e}{X}")

def save_cumulative_results_for_keyword(keyword, all_matches_data):
    keyword_matches = [m for m in all_matches_data if m.get("matched_keyword") == keyword]
    if not keyword_matches: return
    config = get_config()
    folder = os.path.join(config.get("results_dir"), keyword.lower())
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{keyword.lower()}_matches.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(keyword_matches, f, indent=4, ensure_ascii=False)

