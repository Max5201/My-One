from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# 数据库连接（从 Render 环境变量获取）
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# 测试 API
@app.route("/")
def home():
    return jsonify({"message": "Flask + Supabase backend running!"})


# 注册 API
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    hashed_pw = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id",
                    (username, hashed_pw))
        user_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "注册成功", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 登录 API
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        return jsonify({"error": "用户不存在"}), 404

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "密码错误"}), 401

    return jsonify({"message": "登录成功", "username": username}), 200


# 查看用户列表（临时给管理员看，后面可以加密码保护）
@app.route("/users", methods=["GET"])
def users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, created_at FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
