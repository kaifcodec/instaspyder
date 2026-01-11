# headers_loader.py
import json
import os
from instaspyder.core.config_manager import HEADERS_FILE
from instaspyder.utils.colors import R, X

def load_headers():
    """
    Attempts to load headers. 
    Raises FileNotFoundError or ValueError instead of exiting, 
    allowing the main application to handle the missing state.
    """
    try:
        if not os.path.exists(HEADERS_FILE):
            raise FileNotFoundError(f"{HEADERS_FILE} not found.")

        with open(HEADERS_FILE, "r", encoding="utf-8") as header_file:
            headers = json.load(header_file)

            if not headers:
                raise ValueError("Headers file is empty.")

            return headers

    except FileNotFoundError:
        raise
    except (json.JSONDecodeError, ValueError) as e:
        print(f"{R}Error: Could not parse {HEADERS_FILE}. {e}{X}")
        raise
    except Exception as e:
        print(f"{R}An unexpected error occurred while loading headers: {e}{X}")
        raise
