import os
import sys
import urllib.request
import urllib.error
import urllib.parse
import re
import json
import math
from bs4 import BeautifulSoup


client_id = ""
client_secret = ""

def get_blog_count(query, display):
    encode_query = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query
    request = urllib.request.Request(search_url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()
    if (response_code == 200):
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode("utf-8"))

        print("Last build date : " + str(response_body_dict['lastBuildDate']))

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

def get_blog_post(query, display, start_index, sort):
    global no, fs

    encode_query = urllib.parse.quote(query)
    search_url = "https://openapi.naver.com/v1/search/blog?query=" + encode_query +\
                 "&display" + str(display) + "&start" + str(start_index) + "&sort" + str(sort)
    request = urllib.request.Request(search_url)

    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    if response_code is 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode("utf-8"))
        for item_index in range(0, len(response_body_dict["items"])):
            try:
                remove_html_tag = re.compile("<.*?>")
                title = re.sub(remove_html_tag, "", response_body_dict["items"][item_index]["title"])
                link = response_body_dict["items"][item_index]["link"].replace("amp;", "")
                description = re.sub(remove_html_tag, "", response_body_dict["items"][item_index]["description"])
                blogger_name = response_body_dict["items"][item_index]["bloggername"]
                blogger_link = response_body_dict["items"][item_index]["bloggerlink"]

                no += 1
                print("=======================")
                print("#" + str(no))
                print(title)
                print(link)
                print(description)
                print(blogger_name)
                print(blogger_link)

                post_code = request.get(link)
                post_text = post_code.text
                post_soup = BeautifulSoup(post_text, 'lxml')

                for mainFrame in post_soup.select('iframe#mainFrame'):
                    blog_post_url = "http://blog.naver.com" + mainFrame.get('src')
                    blog_post_code = request.get(blog_post_url)
                    blog_post_text = blog_post_code.text
                    blog_post_soup = BeautifulSoup(blog_post_text, 'lxml')

                    for blog_post_content in blog_post_soup.select("div#post-area > div#postListBody"):
                        blog_post_content_text = blog_post_content.get_text()
                        blog_post_full_contents = str(blog_post_content_text)
                        blog_post_full_contents = blog_post_full_contents.replace("\n\n", "\n")
                        print(blog_post_full_contents)

            except:
                item_index += 1



if __name__ == '__main__':
    no = 0
    query = "왕십리 데이트"
    display = 100
    start = 1
    sort = "date"

    fs = open(query + ".txt", "a", encoding="utf-8")

    blog_count = get_blog_count(query, display)
    for start_index in range(start, blog_count + 1, display):
        get_blog_post(query, display, start_index, sort)

    fs.close()
