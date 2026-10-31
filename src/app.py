from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import json

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cameras.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cameras')
def get_cameras():
    conn = get_db()
    cams = conn.execute('SELECT * FROM cameras').fetchall()
    conn.close()
    return jsonify([dict(cam) for cam in cams])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
