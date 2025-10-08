"""
Super minimal Flask test without any dependencies
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({'status': 'working', 'message': 'Python API is alive!'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'server': 'minimal'})

if __name__ == '__main__':
    print("Starting minimal Flask server...")
    try:
        app.run(host='127.0.0.1', port=8083, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)