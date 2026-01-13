# user_id_fetcher.py
import httpx
import json
from instaspyder.utils.colors import C, G, R, Y, X

GENERIC_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Ig-App-Id": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

def get_user_id(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    try:
        with httpx.Client(headers=GENERIC_HEADERS, timeout=10) as client:
            res = client.get(url)

            if res.status_code == 200:
                data = res.json()
                if data.get("data") and data["data"].get("user"):
                    user_id = data["data"]["user"]["id"]
                    print(f"{G}[+] Username: {C}@{username}{G} -> User ID: {user_id} (Fetched as Guest){X}")
                    return user_id
                else:
                    print(f"{Y}[!] User @{username} not found (JSON returned null).{X}")
                    return None

            elif res.status_code == 404:
                print(f"{R}[-] User @{username} does not exist.{X}")
                return None

            else:
                print(f"{R}[-] Failed ({res.status_code}) - Instagram may be blocking this IP or requiring login.{X}")
                return None

    except Exception as e:
        print(f"{R}[-] Exception occurred: {e}{X}")
        return None

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else input("Enter Username: ")
    get_user_id(target)
