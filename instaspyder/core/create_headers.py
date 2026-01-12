import json
import base64
from instaspyder.core.login import login_instagram
from instaspyder.core.config_manager import HEADERS_FILE

USER_AGENT = "Instagram 123.0.0.0 Android (30/11; 480dpi; 1080x2340; samsung; SM-G991B; qcom; en_US)"
APP_ID = "567067343352427"

def generate_bearer_token(ds_user_id, sessionid):
    token_data = {"ds_user_id": str(ds_user_id), "sessionid": str(sessionid)}
    payload = json.dumps(token_data, separators=(',', ':')).encode()
    return f"Bearer IGT:2:{base64.b64encode(payload).decode()}"

def build_header_dictionary(sid, csr, mid, uid):
    """Unified structure for both login and manual entry"""
    auth_string = generate_bearer_token(uid, sid)
    return {
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
        "Cookie": f"csrftoken={csr}; mid={mid}; ig_did={uid}; ig_nrcb=1; sessionid={sid}"
    }

def create_headers_json(username, password):
    try:
        print(f"[*] Authenticating {username}...")
        result = login_instagram(username, password)
        if not result: return False

        sid, csr, mid, uid = result
        final_headers = build_header_dictionary(sid, csr, mid, uid)

        with open(HEADERS_FILE, "w", encoding="utf-8") as f:
            json.dump(final_headers, f, indent=2)
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
