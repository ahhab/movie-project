from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Get the absolute path of the directory where this file is located
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# Define the path to the 'src' directory
SRC_DIR = os.path.join(APP_ROOT, 'src')

@app.route('/')
def serve_index():
    """Serves the index.html file."""
    return send_from_directory(SRC_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serves other static files like CSS and images."""
    return send_from_directory(SRC_DIR, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
