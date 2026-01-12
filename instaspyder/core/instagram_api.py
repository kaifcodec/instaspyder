# instagram_api.py (Modified for Async)
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
        
        if r.status_code == 200:
            return r.json().get("users", [])

        if r.status_code == 400:
            try:
                error_data = r.json()
                if any(k in error_data for k in ["challenge", "checkpoint", "suspended"]):
                    print(f"{R}[!] Global Block: Challenge/Suspension detected on your account.{X}")
                    return "CHECKPOINT_ERROR"
            except json.JSONDecodeError:
                pass

            print(f"{Y}[i] Suggestions disabled or restricted for ID {user_id}. Skipping...{X}")
            return [] 

        if r.status_code == 403:
            print(f"{R}[!] sessionid expired or Login Required (403).{X}")
            return "AUTH_ERROR"

        if r.status_code == 429:
            print(f"{R}[!] Rate limit hit (429).{X}")
            return "RATE_LIMIT_ERROR"

        return []

    except httpx.RequestError as e:
        print(f"{R}Network error while fetching chain for ID {user_id}: {e}{X}")
        return []
    except Exception as e:
        print(f"{R}An unexpected error occurred: {e}{X}")
        return []
