# src/processors/upload_receiver.py
from flask import Flask, request, jsonify
import os
from pathlib import Path

app = Flask(__name__)
UPLOAD_FOLDER = Path("INBOX")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    file.save(UPLOAD_FOLDER / file.filename)
    return jsonify({"status": "received", "file": file.filename})

if __name__ == '__main__':
    app.run(port=5000, debug=True)