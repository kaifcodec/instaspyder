# headers_loader.py
import json
import sys
from assets.config import HEADERS_FILE
from utils.colors import R, X

def load_headers():
    try:
        with open(HEADERS_FILE, "r", encoding="utf-8") as header_file:
            headers = json.load(header_file)
            return headers
    except FileNotFoundError:
        print(f"{R}Error: {HEADERS_FILE} not found. Please run the header generation script first.{X}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{R}Error: Could not parse {HEADERS_FILE}. Ensure it's valid JSON.{X}")
        sys.exit(1)
    except Exception as e:
        print(f"{R}An unexpected error occurred while loading headers: {e}{X}")
        sys.exit(1)

