import requests
from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.parse import quote
import pandas as pd
import urllib

test_link = "https://blog.naver.com/kies84?Redirect=Log&logNo=22264094054"

post_code = urllib.request.urlopen(test_link).read()
post_soup = BeautifulSoup(post_code, 'html.parser')

for mainFrame in post_soup.select('iframe#mainFrame'):
    blog_post_url = "http://blog.naver.com" + mainFrame.get('src')
    blog_post_code = urllib.request.urlopen(blog_post_url).read()
    blog_post_soup = BeautifulSoup(blog_post_code, 'html.parser')

    for post_soup in blog_post_soup.find_all('div', {"id":"postViewBody"}):
        print(post_soup)


