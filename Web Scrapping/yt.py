# coding=utf-8
"""
  YouTube search by CyberTriber (https://github.com/CyberTriber)

          web scrapping with BeautifulSoup example
==============================================================
"""

from bs4 import BeautifulSoup as BS
import requests

base_url = 'https://www.youtube.com/results?search_query='
yt = 'https://youtube.com'

search = input('Hledany vyraz? : ')
url = base_url+search

header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

response = requests.get(url, headers=header)

soup = BS(response.content, 'html.parser')

for link in soup.find_all('a', {'class': 'yt-uix-tile-link'}, href=True, title=True):
    print (link['title'] + ' - '+yt+link['href'])