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
        # STEP 1: Parse the incoming path from the URL
        path = urlparse(self.path).path

        # STEP 2: Handle the root endpoint "/" - just return "OK"
        # TODO: Check if path == "/"
        # TODO: Send 200 response
        # TODO: Set Content-type header to 'text/plain'
        # TODO: End headers
        # TODO: Write b"OK" to self.wfile
        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        
        # STEP 3: 🎯 THE KEY MCP ENDPOINT - "/_mcp/tools"
        # This is where clients discover what tools are available!
        # TODO: Check if path == "/_mcp/tools"
        # TODO: Send 200 response  
        # TODO: Set Content-type header to 'application/json'
        # TODO: End headers
        elif path == "/mcp/tools":
        
            # STEP 4: Define the tools data structure
            # This is the HEART of MCP - servers advertise their capabilities!
            # TODO: Create a list called 'tools' with tool definitions
            # Each tool should have: name, description, and parameters
            # HINT: Each tool is a dictionary with JSON Schema for parameters
            
            tools = [



            ]

            # TODO: Tool 1 - "add" tool
            # - name: "add"
            # - description: "Adds two numbers together."
            # - parameters: JSON Schema object with properties a & b (both numbers)
            
            # TODO: Tool 2 - "substract" tool  
            # - name: "substract"
            # - description: "Subtract two numbers"
            # - parameters: JSON Schema object with properties a & b (both numbers)
            
            # STEP 5: Send the tools as JSON response
            # TODO: Convert tools list to JSON and write to self.wfile
            # HINT: json.dumps(tools, indent=2).encode()
        
        # STEP 6: Handle any other paths with 404
        # TODO: Send 404 response for unrecognized paths
        # TODO: End headers
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