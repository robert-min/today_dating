# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, session, redirect, url_for
import search
from crawling import NaverApi
from time import gmtime, time

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
        keyword = req["userRequest"]["utterance"]
        output = NaverApi(keyword).output_data()
        redirect(url_for("save_page", k_data=keyword))
        # session["keyword"] = keyword
    return jsonify(output)


@app.route("/save_page/<k_data>")
def save_page(k_data):
    print(k_data)
    # tm = gmtime(time())
    # NaverApi(data).save_json(tm)
    # NaverApi(data).save_list(tm)
    # 세션 삭제
    # session.pop(session["keyword"], None)
    return jsonify("clear session")


if __name__ == "__main__":
    app.secret_key = "aksen"
    app.run(host='0.0.0.0') # Flask 기본포트 5000번
