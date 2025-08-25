import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 从环境变量获取数据库连接信息
DATABASE_URL = os.getenv("DATABASE_URL")

@app.route('/message')
def message():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT text FROM messages ORDER BY created_at DESC LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({"message": row[0] if row else "No messages yet!"})
