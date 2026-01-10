# instagram_api.py (Modified for Async)
import httpx
import json
from instaspyder.core.headers_loader import load_headers
from instaspyder.utils.colors import C, G, R, Y, X

HEADERS = load_headers()

async_client = None

async def init_async_client():
    global async_client
    if async_client is None:
        async_client = httpx.AsyncClient(http2=True, headers=HEADERS, timeout=20.0)

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
        r.raise_for_status()
        return r.json().get("users", [])
    except httpx.RequestError as e:
        print(f"{R}Network or request error while fetching chain for ID {user_id}: {e}{X}")
        return []
    except json.JSONDecodeError as e:
        print(f"{R}Failed to parse JSON response for ID {user_id}: {e}.{X}")
        print(f"{Y}   Raw response content: {r.text if 'r' in locals() else 'No response received.'}{X}")
        return []
    except httpx.HTTPStatusError as e:
        print(f"{R}HTTP error {e.response.status_code} while fetching chain for ID {user_id}: {e.response.text}{X}")
        return []
    except Exception as e:
        print(f"{R}An unexpected error occurred while fetching chain for ID {user_id}: {e}{X}")
        return []
