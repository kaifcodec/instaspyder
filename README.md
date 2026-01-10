<p align="center">
  <img src="https://placehold.co/800x250/3498db/ecf0f1?font=Montserrat&text=InstaSpyder%0AFind+Anyone's+Instagram+ID" alt="InstaFinder Banner - Modern Design">
</p>

# 🔍 InstaFinder: Finds Anyone's Instagram ID just by knowing their close ones

**InstaFinder** is a sophisticated and highly modular Python tool designed to explore and discover specific profiles within Instagram's "suggested user" chains. Ever wondered who someone might know, or wanted to find profiles related to certain keywords through a network of connections? This tool helps you do just that, by recursively traversing suggested user lists and identifying matches based on your specified keywords.

---
## 🔒 License

This project is under a **Personal Use Only License**.

- ✅ You may use and modify it **privately** for yourself.
- ❌ You may NOT host it as a public or private service.
- ❌ You may NOT re-upload, fork, or redistribute this code.
- ❌ You may NOT use it in any commercial or monetized way.

- Want to collaborate or get special permissions? Contact me directly kaifcodec@gmail.com
---

## ✨ Features

* **Recursive Chain Exploration:** Dive deep into Instagram's suggested user networks from an initial target profile.
* **Keyword-Based Discovery:** Identify profiles whose usernames or full names match your specified keywords (e.g., "tech," "john doe," "coding").
* **Persistent State Management:** Automatically saves and loads search progress, allowing you to resume interrupted searches without losing data.
* **Organized Results:** Found matches are neatly categorized and saved to dedicated JSON files per keyword.
* **Graceful Exit:** Safely saves all progress and results even if the script is interrupted (e.g., via Ctrl+C).
* **Highly Modular & Maintainable:** Built with a clean, separated architecture for easy understanding, contribution, and future expansion.

---

## 🚀 Getting Started

Follow these steps to get InstaFinder up and running on your local machine.

### Prerequisites

* Python 3.8+
* Git (for cloning the repository)
* A new Instagram account to prevent your known suggestions
### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kaifcodec/InstaFinder.git
    cd InstaFinder
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    All required Python packages are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration**
    Edit the `config.py` file as required to increase the MAX_RECURSION field (default=1)

    - If you think target could be close to user then default value of 1 is recommended or else use 2, 3 or more
    - The higher the value of MAX_RECURSION greater time it will work and could waste time to find inside unknown person's suggestions who might be far in relationship with the target.
      
### `headers.json` Setup (Crucial!)

This tool requires valid Instagram API headers to function. These headers contain authentication tokens and other necessary information to make requests look legitimate.

1.  **Generate `headers.json`:**
    * You will need to manually obtain these headers. The easiest way is to use your browser's developer tools (F12) while logged into Instagram on your mobile browser or desktop.
    * Look for network requests to `i.instagram.com/api/v1/discover/chaining/` or similar API endpoints.
    * Copy the request headers.
    * Save these headers as a JSON object in a file named `headers.json` in the root directory of this project.
    * **Comprehensive `headers.json` example (values will be specific to your session):**
        ```json
        {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
            "Accept-Encoding": "gzip", # case sensitive must not be changed
            "x-ig-app-locale": "en_US",
            "x-ig-device-locale": "en_US",
            "x-ig-mapped-locale": "en_US",
            "x-pigeon-session-id": "your_pigeon_session_id",
            "x-pigeon-rawclienttime": "your_raw_client_time",
            "x-ig-bandwidth-speed-kbps": "12345",
            "x-ig-bandwidth-totalbytes-b": "67890",
            "x-ig-bandwidth-totaltime-ms": "1234",
            "x-bloks-version-id": "your_bloks_version_id",
            "x-ig-www-claim": "your_ig_www_claim",
            "x-bloks-prism-button-version": "your_prism_button_version",
            "x-bloks-prism-colors-enabled": "true",
            "x-bloks-prism-ax-base-colors-enabled": "true",
            "x-bloks-prism-font-enabled": "true",
            "x-bloks-is-layout-rtl": "false",
            "x-ig-device-id": "your_device_id",
            "x-ig-family-device-id": "your_family_device_id",
            "x-ig-android-id": "your_android_id",
            "x-ig-timezone-offset": "19800",
            "x-ig-nav-chain": "your_nav_chain",
            "x-fb-connection-type": "WIFI",
            "x-ig-connection-type": "WIFI",
            "x-ig-capabilities": "your_ig_capabilities",
            "x-ig-app-id": "your_ig_app_id",
            "priority": "u=3",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "your_authorization_token",
            "x-mid": "your_x_mid",
            "ig-u-ds-user-id": "your_ig_u_ds_user_id",
            "ig-u-rur": "your_ig_u_rur",
            "ig-intended-user-id": "your_ig_intended_user_id",
            "x-fb-http-engine": "Liger",
            "x-fb-client-ip": "your_client_ip",
            "x-fb-server-cluster": "your_server_cluster",
        }
        ```

### Running the Tool

Once you have installed dependencies and set up `headers.json`:

```bash
python main.py
```

The script will then prompt you for:
 * An initial Instagram username to start the search from (e.g., a "victim" profile).
 * Keywords/names (comma-separated) to search for in the suggested user profiles, can be name of the target, or there username's some letters.

### ⚠️ Important Considerations & Disclaimers
 * Rate Limiting (feedback_required / HTTP 400/429):
   Instagram aggressively rate-limits API requests to prevent abuse. If you encounter HTTP error 400: {"message":"feedback_required"} or HTTP 429 Too Many Requests, it means your activity has been flagged.
   * To unblock: You MUST manually log in to the Instagram account (whose headers/cookies you are using) via the official Instagram app or website. Complete any CAPTCHA or verification challenges presented. This is Instagram's way of verifying human activity.
   * Prevention: The script includes random delays, but for high-volume usage, you might need to increase these delays, implement more sophisticated adaptive backoff, or use proxy rotation.
 * Ethical Use: This tool is for educational purposes and personal research. Please use it responsibly and ethically. Respect Instagram's Terms of Service. Excessive or abusive use can lead to temporary or permanent bans of your Instagram account or IP address.
 * API Changes: Instagram's private API endpoints can change without notice, which might break the tool's functionality.


