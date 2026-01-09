import json
import hmac
import hashlib
import uuid
import requests
from typing import Optional, Dict, Tuple

V = "v1"
API_URL = "https://i.instagram.com/api/{version}/"
USER_AGENT = "Instagram 123.0.0.0 Android (30/11; 420dpi; 1080x1920; Google; Pixel; sailfish; qcom; en_US)"
IG_SIG_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
SIG_KEY_VERSION = "4"
IG_CAPABILITIES = "3brTvw"
APPLICATION_ID = "567067343352427"
FB_HTTP_ENGINE = "Liger"

def generate_uuid(return_hex: bool = False, seed: Optional[str] = None) -> str:
    if seed:
        m = hashlib.md5()
        m.update(seed.encode("utf-8"))
        new_uuid = uuid.UUID(m.hexdigest())
    else:
        new_uuid = uuid.uuid1()
    return new_uuid.hex if return_hex else str(new_uuid)

def generate_device_id(seed: Optional[str] = None) -> str:
    return "android-%s" % generate_uuid(True, (seed or "")[:16])

def generate_adid(seed: Optional[str] = None, username: Optional[str] = None) -> str:
    modified_seed = seed or username or generate_uuid()
    sha2 = hashlib.sha256()
    sha2.update(modified_seed.encode("utf-8"))
    return generate_uuid(False, sha2.hexdigest())

def default_headers() -> Dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "X-IG-Capabilities": IG_CAPABILITIES,
        "X-IG-App-ID": APPLICATION_ID,
        "X-FB-HTTP-Engine": FB_HTTP_ENGINE,
        "Accept-Language": "en-US",
        "Connection": "close"
    }

def sign_params(params: dict) -> Dict[str, str]:
    json_params = json.dumps(params, separators=(",", ":"))
    mac = hmac.new(IG_SIG_KEY.encode("ascii"), json_params.encode("ascii"), hashlib.sha256).hexdigest()
    return {"ig_sig_key_version": SIG_KEY_VERSION, "signed_body": f"{mac}.{json_params}"}

def get_cookie_value(jar, key):
    for c in jar:
        if c.name.lower() == key.lower():
            return c.value
    return None

class LoginError(Exception): pass

def login_instagram(username, password) -> Tuple[str, str, str, str]:
    s = requests.Session()
    s.headers.update(default_headers())
    pre_url = API_URL.format(version=V) + "si/fetch_headers/"
    try:
        s.post(pre_url, params={"challenge_type": "signup", "guid": generate_uuid(True)}, timeout=10)
    except requests.RequestException as e:
        raise LoginError(f"Prelogin error: {e}")

    csrftoken = get_cookie_value(s.cookies, "csrftoken")
    if not csrftoken: raise LoginError("CSRF missing")

    device_id = generate_device_id()
    login_params = {
        "device_id": device_id,
        "guid": generate_uuid(False),
        "adid": generate_adid(username=username),
        "phone_id": generate_uuid(False, seed=device_id),
        "csrftoken": csrftoken,
        "username": username,
        "password": password,
        "login_attempt_count": 0,
    }

    login_url = API_URL.format(version=V) + "accounts/login/"
    try:
        r = s.post(login_url, data=sign_params(login_params), timeout=20)
        j = r.json()
    except Exception as e:
        raise LoginError(f"Login request failed: {e}")

    if r.status_code != 200 or not j.get("logged_in_user", {}).get("pk"):
        raise LoginError(f"Login failed: {j.get('message', 'Unknown error')}")

    return (
        get_cookie_value(s.cookies, "sessionid"),
        get_cookie_value(s.cookies, "csrftoken"),
        get_cookie_value(s.cookies, "mid"),
        str(j["logged_in_user"]["pk"])
    )
