# api/auth.py
import base64

# Demo credentials
VALID_USERS = {
    "admin": "password123",
    "student": "momo2024",
    "testuser": "test123"
}

def parse_auth_header(auth_header):
    if not auth_header or not auth_header.startswith("Basic "):
        return None, None
    try:
        decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
        return decoded.split(":", 1) if ":" in decoded else (None, None)
    except:
        return None, None

def authenticate(auth_header):
    user, pwd = parse_auth_header(auth_header)
    return user in VALID_USERS and VALID_USERS[user] == pwd

def require_auth(auth_header):
    if not auth_header:
        return False, {"error": "Missing Authorization", "status": 401}
    if not authenticate(auth_header):
        return False, {"error": "Invalid credentials", "status": 401}
    return True, None

# --- Test student style ---
if __name__ == "__main__":
    for creds in ["admin:password123", "admin:wrong", "hacker:123"]:
        encoded = base64.b64encode(creds.encode()).decode()
        header = "Basic " + encoded
        print(creds, "->", " Authenticated" if authenticate(header) else "Failed")
    
    # Test missing header
    auth, resp = require_auth(None)
    print("Missing header ->", " Authenticated" if auth else " Failed", resp)

