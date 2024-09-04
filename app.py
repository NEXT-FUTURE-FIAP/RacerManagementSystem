from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)

def conn_instagram(data):
    username = data.get('username')
    password = data.get('password')
    try:
        cl = Client()
        cl.login(username, password)
        return cl

    except Exception as e:
        print(e)
        return None


# Endpoint para conexão com o Instagram
@app.route('/auth/connect', methods=['POST'])
def connect_instagram():
    try:
        client = conn_instagram(request.json)
        print(client)
        user_id = client.user_id_from_username(client.username)

        if not user_id:
            return jsonify({"coins": 0}), 400

        return jsonify({"coins": 1000}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
