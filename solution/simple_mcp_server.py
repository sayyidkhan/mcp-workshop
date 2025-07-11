#!/usr/bin/env python3
"""
Simple MCP Server using only Python standard library
Perfect for workshops - no dependency issues!
"""

import json
import http.server
import socketserver
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class MCPHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
            
        elif path == "/_mcp/tools":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            tools = [
                {
                    "name": "add",
                    "description": "Adds two numbers together.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "substract",
                    "description": "Subtract two numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"}
                        },
                        "required": ["a", "b"]
                    }
                }
            ]
            
            self.wfile.write(json.dumps(tools, indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        if path == "/add":
            self.handle_add(data)
        elif path == "/substract":
            self.handle_subtract(data)
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_add(self, data):
        """Handle addition tool"""
        a = data.get("a")
        b = data.get("b")
        
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            self.send_error(400, "a and b must be numbers")
            return
        
        result = {
            "result": a + b,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode())
    
    def handle_subtract(self, data):
        """Handle subtraction tool"""
        a = data.get("a")
        b = data.get("b")
        
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            self.send_error(400, "a and b must be numbers")
            return
        
        result = {
            "result": a - b,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode())

if __name__ == "__main__":
    PORT = 8000
    
    with socketserver.TCPServer(("", PORT), MCPHandler) as httpd:
        print(f"🚀 MCP Server running on http://localhost:{PORT}")
        print(f"📋 Tools available at: http://localhost:{PORT}/_mcp/tools")
        test_command = '{"a": 5, "b": 3}'
        print(f"🧮 Test addition: curl -X POST http://localhost:{PORT}/add -H 'Content-Type: application/json' -d '{test_command}'")
        print("Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")