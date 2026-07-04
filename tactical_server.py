"""
Serving the tactical simulator React build within Streamlit.
Uses a background HTTP server to serve static files, then embeds via iframe.
"""

import os
import threading
import http.server
import socketserver
from urllib.parse import urlparse
import streamlit as st

# Absolute path to the built React app
TACTICAL_BUILD_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tactical_build",
)


def get_tactical_url():
    """Start a local HTTP server for the tactical simulator and return its URL.
    
    Returns the base URL (e.g., 'http://localhost:8765') for embedding in an iframe.
    Uses Streamlit session state to persist the server across reruns.
    """
    if "tactical_server_url" not in st.session_state:
        import socket
        
        # Find a free port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()
        
        class TacticalHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=TACTICAL_BUILD_DIR, **kwargs)
            
            def log_message(self, format, *args):
                # Suppress request logs to keep Streamlit console clean
                pass
        
        # Start server in background thread
        socketserver.TCPServer.allow_reuse_address = True
        try:
            server = socketserver.TCPServer(('localhost', port), TacticalHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            st.session_state["tactical_server_url"] = f"http://localhost:{port}"
        except OSError as e:
            if e.errno == 48:  # Address already in use
                st.session_state["tactical_server_url"] = f"http://localhost:{port}"
            else:
                raise
    
    return st.session_state["tactical_server_url"]
