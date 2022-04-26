# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import search
from crawling import NaverApi

app = Flask(__name__)


@app.route('/test', methods=["POST"])
def test():
    if request.method == "POST":
        req = request.get_json()
        print(req)
        keyword = req["action"]["params"]["Subway"]
        temp = search.rds(keyword)
        output = temp.output_data()
    return jsonify(output)

@app.route('/nokeyword', methods=["POST"])
def nokeyword():
    if request.method == "POST":
        req = request.get_json()
        print(req)
        keyword = req["userRequest"]["utterance"]
        print(keyword)
        output = NaverApi.output_data(keyword)
    return jsonify(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0') # Flask 기본포트 5000번