# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import urllib.parse
import json
import math
from bs4 import BeautifulSoup
import time
import secret
from collections import defaultdict


# 네이버 API
client_id = secret.naver_id
client_secret = secret.naver_secret

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


    return blog_count


def get_blog_post(query, display, start_index):
    # OO 데이트로 기본 검색
    encode_query = urllib.parse.quote(query + ' 데이트')
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query + \
                 "&start=" + str(start_index) + "&display=" + str(display)
    request = urllib.request.Request(search_url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    all_contents = defaultdict(list)
    all_contents["keyword"] = query

    if (response_code == 200):
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode("utf-8"))
        contents = response_body_dict["items"]
        all_contents["blog"] = contents
        all_place = list()

        for item_index in range(0, len(contents)):
            link = contents[item_index]["link"]
            ori_link = link.replace("?Redirect=Log&logNo=", "/")
            post_code = urllib.request.urlopen(ori_link).read()
            post_soup = BeautifulSoup(post_code, "lxml")

            for mainFrame in post_soup.select("iframe#mainFrame"):
                blog_post_url = "http://blog.naver.com" + mainFrame.get("src")
                blog_post_code = urllib.request.urlopen(blog_post_url).read()
                blog_post_soup = BeautifulSoup(blog_post_code, "lxml")

                try:
                    map_soup = blog_post_soup.find("div", attrs={"class" : "se-module se-module-map-text"})
                    place_text = map_soup.find("a")["data-linkdata"]
                    place_dict = json.loads(place_text)
                    all_place.append(place_dict)

                except:
                    pass
            item_index += 1
            time.sleep(0.1)

        all_contents["place"] = all_place

    return all_contents

def save_json(query, display, start_index, name):
    all_contents = get_blog_post(query, display, start_index)

    import json
    import os
    from time import time, localtime, strftime

    tm = localtime(time())
    strftime("%Y-%m-%d", tm)

    path = "./date_data/" + strftime("%Y-%m-%d", tm)

    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except OSError as e:
        if e.errno != e.errno.EEXIST:
            print("Failed to create")
            raise

    with open(path + "/{}.json".format(name), "w") as f:
        json.dump(all_contents, f, indent=4, ensure_ascii=False)

# def save_parquet(query, display, start_index):
#     data = get_blog_post(query, display, start_index)
#
#     from pyspark.sql import SparkSession
#
#     MAX_MEMORY = "5g"
#     spark = SparkSession.builder.appName("today_dating") \
#         .config("spark.executor.memory", MAX_MEMORY) \
#         .config("spark.driver.memory", MAX_MEMORY) \
#         .getOrCreate()
#
#     df = spark.createDataFrame(data, schema=None)
#     df.write.json("./")
#
#     print("수집완료")

if __name__ == '__main__':
    query = ["용답", "신답", "용두", "신설동"]
    display = 100
    start = 1
    for i, q in enumerate(query):
        blog_count = get_blog_count(q, display)
        print(q, ":", blog_count)
        for start_index in range(start, blog_count + 1, display):
            print(start_index)
            save_json(q, display, start_index, i)
            print()