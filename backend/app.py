from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/message')
def message():
    return jsonify({"message": "Hello from backend!"})

if __name__ == '__main__':
    app.run()
