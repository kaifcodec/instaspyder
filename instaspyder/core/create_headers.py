import json
import base64
from instaspyder.core.auth import login_instagram
from instaspyder.assets.config import BASE_DIR
# ---------- Modern Pixel 8 Pro Fingerprint (Android 15) ----------
USER_AGENT = "Instagram 123.0.0.0 Android (30/11; 420dpi; 1080x1920; Google; Pixel; sailfish; qcom; en_US)"
APP_ID = "567067343352427"

def generate_bearer_token(ds_user_id, sessionid):
    """Generates a compact, space-less Bearer token to match original structure."""
    token_data = {
        "ds_user_id": str(ds_user_id),
        "sessionid": str(sessionid)
    }
    # Using separators=(',', ':') to remove spaces for a perfect match
    payload = json.dumps(token_data, separators=(',', ':')).encode()
    encoded = base64.b64encode(payload).decode()
    return f"Bearer IGT:2:{encoded}"

def create_headers_json(username, password):
    try:
        print(f"[*] Authenticating {username} as a Modern Pixel device...")
        # Get core session data from your login.py logic
        sessionid, csrftoken, mid, dsuserid = login_instagram(username, password)

        # Build the dynamic Authorization string
        auth_string = generate_bearer_token(dsuserid, sessionid)

        # Final Header structure matching your original working set
        final_headers = {
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "identity",
            "x-ig-app-locale": "en_US",
            "x-ig-device-locale": "en_US",
            "x-ig-mapped-locale": "en_US",
            "x-ig-bandwidth-speed-kbps": "1455.000",
            "x-ig-bandwidth-totalbytes-b": "7783089",
            "x-ig-bandwidth-totaltime-ms": "4901",
            "x-bloks-is-prism-enabled": "true",
            "x-bloks-prism-button-version": "0",
            "x-bloks-is-layout-rtl": "false",
            "x-ig-timezone-offset": "19800",
            "x-fb-connection-type": "WIFI",
            "x-ig-connection-type": "WIFI",
            "x-ig-capabilities": "3brTv10=",
            "x-ig-app-id": APP_ID,
            "priority": "u=3",
            "accept-language": "en-US",
            "authorization": auth_string,
            "x-fb-http-engine": "Liger",
            "x-fb-client-ip": "True",
            "x-fb-server-cluster": "True",
            "Cookie": f"csrftoken={csrftoken}; mid={mid}; ig_did={dsuserid}; ig_nrcb=1"
        }

        # Write to headers.json
        with open(BASE_DIR / "headers.json", "w", encoding="utf-8") as f:
            json.dump(final_headers, f, indent=2)

        print("[+] headers.json created successfully with Modern Pixel footprint.")

    except Exception as e:
        print(f"[!] Critical Error: {e}")

if __name__ == "__main__":
    u = input("Username: ")
    p = input("Password: ")
    create_headers_json(u, p)
















