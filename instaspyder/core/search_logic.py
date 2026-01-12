# search_logic.py (Modified for Async - cleaner output)
import asyncio
import random
from instaspyder.core.instagram_api import fetch_chain_async
from instaspyder.core.user_id_fetcher import get_user_id
from instaspyder.core.config_manager import get_config
from instaspyder.utils.sanitize_text import sanitize_text
from instaspyder.utils.colors import C, G, R, Y, X

async def recursive_chain_search_async(username, keywords_to_match, visited_users, all_found_matches, depth=0, known_user_id=None, depth_limit=None):
    indent = "  " * depth

    # Fallback logic: if no limit was passed from main, check config
    if depth_limit is None:
        config = get_config()
        depth_limit = config.get("max_depth", 2)

    if depth > depth_limit:
        return

    user_id = known_user_id
    if user_id is None:
        user_id = get_user_id(username)

    if not user_id:
        print(f"{indent}{R}Could not get user ID for @{username}. Skipping this user.{X}")
        return

    if depth > 0 and user_id in visited_users:
        return

    visited_users.add(user_id)
    print(f"{indent}{C}Searching chains of @{username} (ID: {user_id})... [Depth: {depth}/{depth_limit}]{X}")

    users_in_chain = await fetch_chain_async(user_id)

    if isinstance(users_in_chain, str) and "_ERROR" in users_in_chain:
        raise Exception(f"Instagram Block: {users_in_chain}")

    if not users_in_chain:
        print(f"{indent}{Y}No users found in chain for @{username}{X}")
        return

    for user_data in users_in_chain:
        uname = user_data.get("username", "")
        fname = user_data.get("full_name", "")
        uid = user_data.get("id")

        if not uname or not uid:
            continue

        clean_uname = sanitize_text(uname).lower()
        clean_fname = sanitize_text(fname).lower()

        for kw_to_check in keywords_to_match:
            clean_kw = sanitize_text(kw_to_check).lower()
            if clean_kw in clean_uname or clean_kw in clean_fname:
                match_data = {
                    "username": uname,
                    "full_name": fname,
                    "user_id": uid,
                    "found_via_username": username,
                    "found_via_user_id": user_id,
                    "depth_found": depth,
                    "matched_keyword": kw_to_check
                }

                if match_data not in all_found_matches:
                    all_found_matches.append(match_data)
                    print(f"\n{G}" + "="*60)
                    print(f"FOUND MATCH for '{kw_to_check}'!")
                    print(f"   User: {C}@{uname}{X} - {fname}")
                    print(f"   ID: {uid}")
                    print(f"   Found via: @{username} (Depth {depth})")
                    print(f"{G}" + "="*60 + f"{X}\n")

    if depth < depth_limit:
        tasks = []
        for user_data in users_in_chain:
            await asyncio.sleep(random.uniform(0.1, 0.2))
            tasks.append(
                recursive_chain_search_async(
                    user_data["username"],
                    keywords_to_match,
                    visited_users,
                    all_found_matches,
                    depth + 1,
                    known_user_id=user_data.get("id"),
                    depth_limit=depth_limit # Pass the limit down the chain
                )
            )
        if tasks:
            await asyncio.gather(*tasks)
