from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
users_path = "users.json"

# 유저 정보 불러오기
def load_users():
    if not os.path.exists(users_path):
        return {}
    with open(users_path, "r") as f:
        return json.load(f)

# 유저 정보 저장
def save_users(users):
    with open(users_path, "w") as f:
        json.dump(users, f)

# ✅ 회원가입
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    users = load_users()
    if data["id"] in users:
        return jsonify(success=False, message="이미 존재하는 아이디입니다.")
    users[data["id"]] = {"pw": data["pw"], "score": 1000}
    save_users(users)
    return jsonify(success=True)

# ✅ 로그인
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    users = load_users()
    if data["id"] in users and users[data["id"]]["pw"] == data["pw"]:
        return jsonify(success=True, score=users[data["id"]]["score"])
    return jsonify(success=False, message="아이디 또는 비밀번호 오류")

# ✅ 점수 갱신 (승패 반영)
@app.route("/update_score", methods=["POST"])
def update_score():
    data = request.get_json()
    users = load_users()
    if data["id"] in users:
        users[data["id"]]["score"] += int(data["delta"])
        save_users(users)
        return jsonify(success=True, new_score=users[data["id"]]["score"])
    return jsonify(success=False, message="존재하지 않는 유저")

# ✅ 점수 조회 (선택 사항)
@app.route("/score/<userid>", methods=["GET"])
def get_score(userid):
    users = load_users()
    if userid in users:
        return jsonify(success=True, score=users[userid]["score"])
    return jsonify(success=False, message="유저 없음")

if __name__ == "__main__":
    app.run(port=3001)