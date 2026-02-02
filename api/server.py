"""
REST API Server for Mobile Money Transactions
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
from urllib.parse import urlparse, parse_qs

# Import the modules
from auth import require_auth
from routes import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction,
    get_transaction_stats
)


class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API"""

    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def _send_response(self, data, status_code=200):
        self._set_headers(status_code)
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode())

    def _send_error_response(self, message, status_code=400):
        self._send_response({
            "status": "error",
            "message": message,
            "error_code": status_code
        }, status_code)

    def _check_auth(self):
        auth_header = self.headers.get('Authorization')
        is_auth, error = require_auth(auth_header)
        if not is_auth:
            self._send_response(error, 401)
            return False
        return True

    def _parse_path(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        match = re.match(r'^/transactions/(\d+)$', path)
        if match:
            return '/transactions', int(match.group(1))
        return path, None

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        if not self._check_auth():
            return
        path, transaction_id = self._parse_path()

        if self.path.rstrip('/') == '/transactions/stats':
            result = get_transaction_stats()
            self._send_response(result)
        elif transaction_id is not None:
            result = get_transaction_by_id(transaction_id)
            status = 404 if result.get('error_code') == 404 else 200
            self._send_response(result, status)
        elif path == '/transactions':
            result = get_all_transactions()
            self._send_response(result)
        else:
            self._send_error_response("Endpoint not found", 404)

    def do_POST(self):
        if not self._check_auth():
            return
        path, _ = self._parse_path()
        if path != '/transactions':
            self._send_error_response("Endpoint not found", 404)
            return
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            self._send_error_response("Request body required", 400)
            return
        try:
            body = self.rfile.read(length)
            data = json.loads(body.decode())
            result = create_transaction(data)
            status = 400 if result.get('error_code') == 400 else 201
            self._send_response(result, status)
        except Exception as e:
            self._send_error_response("Invalid JSON or server error: {}".format(str(e)), 400)

    def do_PUT(self):
        if not self._check_auth():
            return
        path, transaction_id = self._parse_path()
        if transaction_id is None:
            self._send_error_response("Transaction ID required", 400)
            return
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            self._send_error_response("Request body required", 400)
            return
        try:
            body = self.rfile.read(length)
            data = json.loads(body.decode())
            result = update_transaction(transaction_id, data)
            status = 404 if result.get('error_code') == 404 else 200
            self._send_response(result, status)
        except Exception as e:
            self._send_error_response("Invalid JSON or server error: {}".format(str(e)), 400)

    def do_DELETE(self):
        if not self._check_auth():
            return
        path, transaction_id = self._parse_path()
        if transaction_id is None:
            self._send_error_response("Transaction ID required", 400)
            return
        result = delete_transaction(transaction_id)
        status = 404 if result.get('error_code') == 404 else 200
        self._send_response(result, status)

    def log_message(self, format, *args):
        # Python 3.5 compatible logging
        print("[{}] {}".format(self.log_date_time_string(), format % args))


def run_server(host='localhost', port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    print("="*60)
    print("Mobile Money Transaction API Server")
    print("="*60)
    print("Server running on http://{}:{}".format(host, port))
    print("Press Ctrl+C to stop server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()


if __name__ == "__main__":
    run_server()

