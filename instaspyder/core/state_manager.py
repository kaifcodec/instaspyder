import json
import os
from instaspyder.core.config_manager import get_config, USER_HOME
from instaspyder.utils.colors import C, G, R, Y, X

def _get_state_filepath(username):
    safe_username = "".join(c for c in username if c.isalnum())
    return os.path.join(USER_HOME, f"search_state_{safe_username}.json")

def load_search_state(initial_username, current_keywords=None):
    visited_users = set()
    all_found_matches = []
    state_filepath = _get_state_filepath(initial_username)

    try:
        with open(state_filepath, "r", encoding="utf-8") as f:
            state = json.load(f)
            
            # Check if this state belongs to the same user
            if state.get("initial_username") == initial_username:
                saved_keywords = state.get("keywords", [])
                
                # If keywords have changed, the old 'visited' list is irrelevant for a new search
                if current_keywords and set(current_keywords) != set(saved_keywords):
                    print(f"{Y}[!] Keywords changed from {saved_keywords} to {current_keywords}.{X}")
                    print(f"{C}[i] Ignoring previous visited history to ensure new keywords are checked.{X}")
                    # We keep the found_matches but clear visited to allow re-scanning
                    all_found_matches = state.get("found_matches", [])
                    return set(), all_found_matches

                visited_users = set(state.get("visited", []))
                all_found_matches = state.get("found_matches", [])
                print(f"{G}[+] Loaded previous state for '{initial_username}'. Resuming general search...{X}")
                print(f"   Total visited users: {len(visited_users)}")
                print(f"   Total matches found so far: {len(all_found_matches)}")
            else:
                print(f"{Y}[!] Saved state found at {state_filepath} but for a different initial user. Starting fresh.{X}")

    except FileNotFoundError:
        print(f"{C}[i] No previous search state found at {state_filepath}. Starting fresh for '{initial_username}'.{X}")
    except json.JSONDecodeError:
        print(f"{R}[!] Corrupted state file detected at {state_filepath}. Starting fresh.{X}")
        try:
            os.remove(state_filepath)
        except OSError:
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
        "keywords": keywords # Save keywords to detect changes later
    }
    try:
        with open(state_filepath, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4, ensure_ascii=False)
        print(f"\n{G}[+] Search state saved to {state_filepath}{X}")
    except Exception as e:
        print(f"{R}[-] Error saving state to {state_filepath}: {e}{X}")

def save_cumulative_results_for_keyword(keyword, all_matches_data):
    keyword_matches = [m for m in all_matches_data if m.get("matched_keyword") == keyword]
    if not keyword_matches:
        print(f"{C}[i] No matches found for keyword '{keyword}'. Skipping saving.{X}")
        return

    config = get_config()
    cumulative_results_dir = config.get("results_dir")

    folder = os.path.join(cumulative_results_dir, keyword.lower())
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"{keyword.lower()}_matches.json")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(keyword_matches, f, indent=4, ensure_ascii=False)
        print(f"{G}[+] Matches for '{keyword}' saved to {filepath}{X}")
    except Exception as e:
        print(f"{R}[-] Error saving cumulative results for '{keyword}' to {filepath}: {e}{X}")

