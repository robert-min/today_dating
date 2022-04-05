from flask import Flask, request, jsonify
import sys
app = Flask(__name__)


@app.route('/test', methods=["POST"])
def test():
    if request.method == "POST":
        req = request.get_json()
        print(req)
        keyword = req["action"]["params"]["Subway"]
        print(keyword)
        output = list_card(keyword)
    return jsonify(output)


def list_card(temp):
    output = {
      "version": "2.0",
      "template": {
        "outputs": [
          {
            "listCard": {
              "header": {
                "title": "{} 데이트 장소 입니다.".format(temp)
              },
              "items": [
                {
                  "title": "챗봇 관리자센터",
                  "description": "새로운 AI의 내일과 일상의 변화",
                  "link": {
                    "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                  }
                },
                {
                  "title": "챗봇 관리자센터",
                  "description": "카카오톡 채널 챗봇 만들기",
                  "link": {
                    "web": "https://namu.wiki/w/%EB%AC%B4%EC%A7%80(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                  }
                },
                {
                  "title": "Kakao i Voice Service",
                  "description": "보이스봇 / KVS 제휴 신청하기",
                  "link": {
                    "web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
                  }
                },
                  {
                  "title": "Kakao i Voice Service",
                  "description": "보이스봇 / KVS 제휴 신청하기",
                  "link": {
                    "web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
                  }
                },
                  {
                  "title": "Kakao i Voice Service",
                  "description": "보이스봇 / KVS 제휴 신청하기",
                  "link": {
                    "web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
                  }
                }
              ]
            }
          },
            {"simpleText": {
               "text": "추가 검색을 원하실 경우\n키워드를 입력해주세요."}}
        ]
      }
    }
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0') # Flask 기본포트 5000번