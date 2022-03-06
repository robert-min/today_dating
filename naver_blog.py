# blog_DB : keyword, title, link, placeId -> json
# place_DB : placeId, name, address, latitude, longitude, tel -> json
import urllib.request
import urllib.error
import urllib.parse
import re
import json
import math
from bs4 import BeautifulSoup
import time

# 네이버 API(git 업로드시 삭제)
client_id = "erQtIDkUqelPooBmJ5r4"
client_secret = "jAVQyNK_Q4"

def get_blog_count(query, display):
    # OO 데이트로 기본 검색
    encode_query = urllib.parse.quote(query + '데이트')
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query
    request = urllib.request.Request(search_url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    if (response_code == 200):
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode("utf-8"))

        print("Last blog build date : " + str(response_body_dict["lastBuildDate"]))

        if response_body_dict["total"] == 0:
            blog_count = 0
        else:
            blog_total = math.ceil(response_body_dict["total"] / int(display))

            if blog_total >= 1000:
                blog_count = 1000
            else:
                blog_count = blog_total

            print("Blog total : " + str(blog_total))
            print("Blog count : " + str(blog_count))

            search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query + \
                         "&display=" + str(100) + "&start=" + str(1) + "&sort=" + "date"
            print(search_url)

    return blog_count

def get_blog_post(query, display, start_index, sort):

    # OO 데이트로 기본 검색
    encode_query = urllib.parse.quote(query + ' 데이트')
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query
    request = urllib.request.Request(search_url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()
    print(response_code)

    if (response_code == 200):
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode("utf-8"))

        for item_index in range(0, len(response_body_dict["items"])):
            remove_tag = re.compile("<.*?>")
            keyword = str(query)
            title = re.sub(remove_tag, "", response_body_dict["items"][item_index]["title"])
            link = response_body_dict["items"][item_index]["link"]
            ori_link = link.replace("?Redirect=Log&logNo=", "/")

            post_code = urllib.request.urlopen(ori_link).read()
            post_soup = BeautifulSoup(post_code, "lxml")

            for mainFrame in post_soup.select("iframe#mainFrame"):
                blog_post_url = "http://blog.naver.com" + mainFrame.get("src")
                blog_post_code = urllib.request.urlopen(blog_post_url).read()
                blog_post_soup = BeautifulSoup(blog_post_code, "lxml")

                try:
                    for map_soup in blog_post_soup.find_all("div", attrs={"class" : "se-module se-module-map-text"}):
                        place_text = map_soup.find("a")["data-linkdata"]
                        place = json.loads(place_text)
                        blog_dict = {"keyword": keyword, "title": title, "link": ori_link,
                                     "placeId": int(place["placeId"])}
                except:
                    blog_dict = {"keyword": keyword, "title": title, "link": ori_link}

            blog = json.dumps(blog_dict)

            print(place)
            print(blog)

            item_index += 1
            time.sleep(0.5)



if __name__ == '__main__':
    query = "왕십리"
    display = 100
    start = 1
    sort = "date"

    blog_count = get_blog_count(query, display)
    for start_index in range(start, blog_count + 1, display):
        get_blog_post(query, display, start_index, sort)
