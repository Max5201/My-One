import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Render 上配置环境变量 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

@app.route("/message")
def get_message():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT text, created_at FROM messages ORDER BY created_at DESC LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({
        "text": row[0],
        "created_at": row[1].isoformat() if row else None
    })
