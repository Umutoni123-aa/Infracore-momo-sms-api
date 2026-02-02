"""
Basic Authentication Module
Validates user credentials using HTTP Basic Auth
"""

import base64

# Simple user database (in production, use a real database with hashed passwords)
VALID_USERS = {
    "admin": "password123",
    "student": "momo2024",
    "testuser": "test123"
}

def parse_auth_header(auth_header):
    """Extract username and password from Authorization header"""
    if not auth_header or not auth_header.startswith("Basic "):
        return None, None
    try:
        decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
        return decoded.split(":", 1) if ":" in decoded else (None, None)
    except:
        return None, None

def authenticate(headers):
    """
    Authenticate user based on HTTP Basic Auth
    
    Args:
        headers: Request headers (dict-like object)
    
    Returns:
        dict: Authentication result with status and error message
    """
    # Get Authorization header
    auth_header = headers.get('Authorization', '')
    
    # Parse credentials
    username, password = parse_auth_header(auth_header)
    
    # Check if credentials are valid
    if username and username in VALID_USERS and VALID_USERS[username] == password:
        return {
            'status': 200,
            'message': 'Authenticated',
            'user': username
        }
    
    # Invalid credentials
    if not auth_header:
        return {
            'status': 401,
            'error': 'Missing Authorization',
            'message': 'Authorization header required'
        }
    else:
        return {
            'status': 401,
            'error': 'Invalid Credentials',
            'message': 'Username or password incorrect'
        }


# Test function
if __name__ == "__main__":
    print("Basic Authentication Test")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {"Authorization": "Basic " + base64.b64encode(b"admin:password123").decode()},
        {"Authorization": "Basic " + base64.b64encode(b"admin:wrong").decode()},
        {"Authorization": "Basic " + base64.b64encode(b"hacker:123").decode()},
        {}
    ]
    
    for i, headers in enumerate(test_cases, 1):
        result = authenticate(headers)
        status = "✓" if result['status'] == 200 else "✗"
        print(f"{status} Test {i}: {result}")
