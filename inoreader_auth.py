import secrets
from http.server import BaseHTTPRequestHandler
from typing import Any

CLIENT_ID = "your_app_id"
CLIENT_SECRET = "your_app_key"
REDIRECT_URI = "http://localhost:8765/callback"
SCOPE = "read"

AUTH_URL = "https://www.inoreader.com/oauth2/auth"
TOKEN_URL = "https://www.inoreader.com/oauth2/token"

state = secrets.token_urlsafe(16)
result: dict[Any, Any] = {}

class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pass