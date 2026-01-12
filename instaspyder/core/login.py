import json
import hashlib
import uuid
import hmac
import httpx
from instaspyder.utils.colors import R, X, C

V = "v1"
API_URL = "https://i.instagram.com/api/{version}/"
USER_AGENT = "Instagram 123.0.0.0 Android (30/11; 480dpi; 1080x2340; samsung; SM-G991B; qcom; en_US)"
IG_SIG_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
SIG_KEY_VERSION = "4"

class LoginError(Exception): pass

def gen_uuid(h=False, s=None):
    if s:
        m = hashlib.md5(s.encode()).hexdigest()
        u = uuid.UUID(m)
    else:
        u = uuid.uuid1()
    return u.hex if h else str(u)

def sign(p):
    j = json.dumps(p, separators=(",", ":"))
    m = hmac.new(IG_SIG_KEY.encode(), j.encode(), hashlib.sha256).hexdigest()
    return {"ig_sig_key_version": SIG_KEY_VERSION, "signed_body": f"{m}.{j}"}

def get_c(jar, k):
    return jar.get(k)

def login_instagram(u, p):
    s = httpx.Client(headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US"})

    try:
        s.post(f"{API_URL.format(version=V)}si/fetch_headers/", params={"guid": gen_uuid(True)}, timeout=10)
        csrf = get_c(s.cookies, "csrftoken")
        if not csrf: raise LoginError("CSRF missing")

        did = f"android-{gen_uuid(True, u[:16])}"
        payload = {
            "device_id": did,
            "guid": gen_uuid(),
            "adid": gen_uuid(False, hashlib.sha256(u.encode()).hexdigest()),
            "phone_id": gen_uuid(False, did),
            "csrftoken": csrf,
            "username": u,
            "password": p,
            "login_attempt_count": 0,
        }

        r = s.post(f"{API_URL.format(version=V)}accounts/login/", data=sign(payload), timeout=20)
        j = r.json()

        if r.status_code != 200 or "logged_in_user" not in j:
            raise LoginError(j.get("message", "Login failed"))

        return (
            get_c(s.cookies, "sessionid"),
            get_c(s.cookies, "csrftoken"),
            get_c(s.cookies, "mid"),
            str(j["logged_in_user"]["pk"])
        )
    except Exception as e:
        print(f"{R}Login Error: {e}{X}")
        return None
