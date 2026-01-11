# instagram_api.py
import httpx
import json
from instaspyder.core.headers_loader import load_headers
from instaspyder.utils.colors import C, G, R, Y, X

async_client = None

async def init_async_client():
    global async_client
    if async_client is None:
        headers = load_headers()
        async_client = httpx.AsyncClient(http2=True, headers=headers, timeout=20.0)


async def close_async_client():
    global async_client
    if async_client:
        await async_client.aclose()
        async_client = None

async def fetch_chain_async(user_id):
    if async_client is None:
        await init_async_client()

    url = f"https://i.instagram.com/api/v1/discover/chaining/?module=profile&target_id={user_id}&profile_chaining_check=false"
    try:
        r = await async_client.get(url)
        print(f"{G}[+] Status for User ID {user_id}: {r.status_code}{X}")
        
        if r.status_code == 403:
            print(f"{R}[!] sessionid expired or Login Required (403).{X}")
            return "AUTH_ERROR"
        
        if r.status_code == 400:
            if "challenge_required" in r.text or "suspended" in r.text:
                print(f"{R}[!] Account Flagged or Challenge Required (400).{X}")
                return "CHECKPOINT_ERROR"
            return "RATE_LIMIT_ERROR"

        r.raise_for_status()
        return r.json().get("users", [])

    except httpx.RequestError as e:
        print(f"{R}Network or request error while fetching chain for ID {user_id}: {e}{X}")
        return []
    except json.JSONDecodeError as e:
        print(f"{R}Failed to parse JSON response for ID {user_id}: {e}.{X}")
        return []
    except httpx.HTTPStatusError as e:
        # Extra safety for any other HTTP errors not caught above
        print(f"{R}HTTP error {e.response.status_code} while fetching chain for ID {user_id}: {e.response.text}{X}")
        if e.response.status_code in [400, 403, 429]:
            return "GENERIC_BLOCK_ERROR"
        return []
    except Exception as e:
        print(f"{R}An unexpected error occurred while fetching chain for ID {user_id}: {e}{X}")
        return []
