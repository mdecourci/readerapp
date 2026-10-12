import secrets
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import requests

CLIENT_ID = "your_app_id"        # App ID
CLIENT_SECRET = "your_app_key"   # App Key
REDIRECT_URI = "http://localhost:8765/callback"  # must match the app settings exactly
SCOPE = "read"

AUTH_URL = "https://www.inoreader.com/oauth2/auth"
TOKEN_URL = "https://www.inoreader.com/oauth2/token"

state = secrets.token_urlsafe(16)
result: dict[Any, Any] = {}

class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        result["code"] = query.get("code", [None])[0]
        result["state"] = query.get("state", [None])[0]
        result["error"] = query.get("error", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Authorised. You can close this tab and return to PyCharm.")

    def log_message(self, *args):
        pass  # keep the console clean


def main():
    # 1. Open the consent page in your browser
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": state,
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    print("Opening browser. If nothing opens, visit:\n", url)
    webbrowser.open(url)

    # 2. Wait for Inoreader to redirect back to localhost
    server = HTTPServer(("localhost", 8765), CallbackHandler)
    server.handle_request()
    server.server_close()

    if result.get("error") or not result.get("code"):
        raise SystemExit(f"Authorisation failed: {result.get('error') or 'no code returned'}")
    if result.get("state") != state:
        raise SystemExit("State mismatch - aborting.")

    # 3. Exchange the code for tokens
    resp = requests.post(
        TOKEN_URL,
        data={
            "code": result["code"],
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "",
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    print("HTTP status:", resp.status_code)
    resp.raise_for_status()
    tokens = resp.json()

    print("Access token: ", tokens.get("access_token"))
    print("Refresh token:", tokens.get("refresh_token"))
    print("Expires in (s):", tokens.get("expires_in"))


if __name__ == "__main__":
    main()
