import os
from pathlib import Path

# Path to this folder
BASE_DIR = Path(__file__).resolve().parent

HEADERS_FILE = str(BASE_DIR / "headers.json")
STATE_FILE_TEMPLATE = "search_state_{}.json"
CUMULATIVE_RESULTS_DIR = "results"
MAX_DEPTH = 1  # Maximum recursion depth for chain exploration (0 for searching only the victim's suggestions)
