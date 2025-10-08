"""
Minimal test Flask app
"""
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({'message': 'Hello from Python!', 'timestamp': time.time()})

if __name__ == '__main__':
    print("Starting minimal Flask test...")
    app.run(host='127.0.0.1', port=8083, debug=False)