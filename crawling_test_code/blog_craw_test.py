from bs4 import BeautifulSoup
from urllib.request import Request
import urllib
import json

test_link = 'https://blog.naver.com/thdwb92?Redirect=Log&logNo=221920115591'
url_link = test_link.replace("?Redirect=Log&logNo=", "/")

post_code = urllib.request.urlopen(url_link).read()
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

