#!/usr/bin/env python3
"""
Ultra-basic Flask test to isolate the crash issue
"""

import sys
print(f"Python version: {sys.version}")

try:
    from flask import Flask
    print("Flask imported successfully")
    
    app = Flask(__name__)
    print("Flask app created")
    
    @app.route('/health')
    def health():
        return "OK"
    
    print("Route registered")
    
    if __name__ == '__main__':
        print("About to start Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()