from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # 允许跨域访问（前端才能正常调用）

# 从环境变量读取 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn

# ✅ 获取所有消息
@app.route("/messages", methods=["GET"])
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text, created_at FROM messages ORDER BY id DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    messages = []
    for row in rows:
        messages.append({
            "id": row[0],
            "text": row[1],
            "created_at": row[2].isoformat()
        })

    return jsonify(messages)

# ✅ 新增一条消息
@app.route("/add", methods=["POST"])
def add_message():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "text is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (text) VALUES (%s) RETURNING id, created_at;", (text,))
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": new_row[0],
        "text": text,
        "created_at": new_row[1].isoformat()
    })

@app.route("/")
def home():
    return jsonify({"message": "Flask + Supabase backend running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
