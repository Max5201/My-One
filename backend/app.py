from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# 从环境变量获取 Supabase 数据库连接字符串
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return jsonify({"message": "Flask + Supabase backend running!"})

# --- 测试数据库连接 ---
@app.route("/db-test")
def db_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        now = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"message": "数据库连接成功 ✅", "time": str(now)})
    except Exception as e:
        print("数据库连接失败:", e)
        return jsonify({"error": str(e)}), 500

# --- 注册 ---
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")  # ⚠️ 简单存储，后面要加 hash

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 插入用户
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
            (username, password)
        )
        user_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "注册成功 🎉", "user_id": user_id, "username": username})
    except Exception as e:
        print("注册错误:", e)
        return jsonify({"error": str(e)}), 500   # 返回真实错误信息

# --- 登录 ---
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, username FROM users WHERE username=%s AND password=%s;",
            (username, password)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return jsonify({"message": "登录成功 ✅", "user_id": user[0], "username": user[1]})
        else:
            return jsonify({"error": "用户名或密码错误"}), 401
    except Exception as e:
        print("登录错误:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
