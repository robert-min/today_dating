import os
import sys
import urllib.request
import pandas as pd
import json
import re

test_df = pd.DataFrame(columns=("search_word", "title", "link", "description"))

client_id = ""
client_secret = ""

search_word = urllib.parse.quote(input("검색어"))
display = 100
start = 1
end = 1000
df_idx = 0

for idx in range(start, end, display):

    url = "https://openapi.naver.com/v1/search/blog?query=" + search_word \
            + "&display=" + str(display) \
            + "&start=" + str(idx)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        response_dict = json.loads(response_body.decode("utf-8"))
        items = response_dict["items"]
        for items_idx in range(0, len(items)):
            remove_tag = re.compile("<.*?>")
            title = re.sub(remove_tag, "", items[items_idx]["title"])
            link = items[items_idx]["link"]
            description = re.sub(remove_tag, "", items[items_idx]["description"])
            test_df.loc[df_idx] = [search_word, title, link, description]
            df_idx += 1
    else:
        print("Error Code" + rescode)

test_df