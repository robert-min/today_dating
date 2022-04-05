# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import search


app = Flask(__name__)


@app.route('/test', methods=["POST"])
def test():
    if request.method == "POST":
        req = request.get_json()
        print(req)
        keyword = req["action"]["params"]["Subway"]
        print(keyword)
        temp = search.rds(keyword)
        output = temp.find_data()
    return jsonify(output)



if __name__ == "__main__":
    app.run(host='0.0.0.0') # Flask 기본포트 5000번