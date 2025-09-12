from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 방 목록 저장용 리스트
rooms = []

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    global rooms

    # ✅ 같은 IP+Port 방 중복 등록 방지
    rooms = [room for room in rooms if room["ip"] != data["ip"] or room["port"] != data["port"]]

    rooms.append(data)
    print(f"📥 등록된 방: {data}")
    return jsonify(success=True)

@app.route("/unregister", methods=["POST"])
def unregister():
    data = request.get_json()
    global rooms

    # ✅ IP+Port 기준으로 정확히 제거
    rooms = [room for room in rooms if room["ip"] != data["ip"] or room["port"] != data["port"]]

    print(f"🗑️ 해제된 방: {data}")
    return jsonify(success=True)

@app.route("/rooms", methods=["GET"])
def get_rooms():
    return jsonify(rooms)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)