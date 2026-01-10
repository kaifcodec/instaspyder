import json
import os
from pathlib import Path

USER_HOME = Path.home() / ".instaspyder"
CONFIG_FILE = USER_HOME / "config.json"
HEADERS_FILE = USER_HOME / "headers.json"

DEFAULT_CONFIG = {
    "max_depth": 2,
    "results_dir": str(USER_HOME / "results"),
    "save_state": True
}

def init_env():
    """Ensures the config folder and files exist."""
    USER_HOME.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
    if not HEADERS_FILE.exists():
        with open(HEADERS_FILE, 'w') as f:
            json.dump({}, f)

def get_config():
    init_env()
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def update_config(key, value):
    config = get_config()
    config[key] = value
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def save_raw_headers(json_stack):
    """Saves the dict/json to headers.json."""
    init_env()
    with open(HEADERS_FILE, 'w') as f:
        json.dump(json_stack, f, indent=4)

def check_headers():
    """Returns True if headers.json has valid content, else False."""
    init_env()
    try:
        with open(HEADERS_FILE, 'r') as f:
            data = json.load(f)
            return isinstance(data, dict) and len(data) > 0
    except (json.JSONDecodeError, FileNotFoundError):
        return False
