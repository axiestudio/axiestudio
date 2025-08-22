#!/usr/bin/env python3
"""
Simple HTTP server to test the showcase functionality
"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

# Set the port
PORT = 8000

# Change to the temp directory to serve files
os.chdir(Path(__file__).parent)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🚀 Test server starting at http://localhost:{PORT}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print(f"🎯 Test showcase at: http://localhost:{PORT}/test_showcase.html")
            print(f"📊 Store index at: http://localhost:{PORT}/src/frontend/public/store_components_converted/store_index.json")
            print("\n✅ Server ready! Press Ctrl+C to stop.")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
