from bs4 import BeautifulSoup
from urllib.request import Request
import urllib
import json

test_link = 'https://openapi.naver.com/v1/search/blog?query=%EC%99%95%EC%8B%AD%EB%A6%AC%20%EB%8D%B0%EC%9D%B4%ED%8A%B8&start=101&display=100'

post_code = urllib.request.urlopen(test_link).read()
post_soup = BeautifulSoup(post_code, 'lxml')

for mainFrame in post_soup.select('iframe#mainFrame'):
    print(mainFrame.get('src'))
    blog_post_url = "http://blog.naver.com" + mainFrame.get('src')
    blog_post_code = urllib.request.urlopen(blog_post_url).read()
    blog_post_soup = BeautifulSoup(blog_post_code, 'lxml')

    for post_soup in blog_post_soup.find_all('div', attrs={'class' : 'se-module se-module-map-text'}):
        text_place = post_soup.find('a')['data-linkdata']
        place = json.loads(text_place)
        print(place)

