from flask import Flask, request, jsonify
import sys
app = Flask(__name__)


@app.route('/test', methods=["POST"])
def test():
    dataSend = request.get_json()
    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='0.0.0.0') # Flask 기본포트 5000번