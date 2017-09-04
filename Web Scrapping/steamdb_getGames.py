# coding=utf-8
"""
  Steam games by CyberTriber (https://github.com/CyberTriber)

          web scrapping with BeautifulSoup example
==============================================================
"""

from bs4 import BeautifulSoup as BS
import requests

url = 'https://steamdb.info/sales/'
header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
response = requests.get(url, headers=header)
soup = BS(response.content, 'html.parser')

prices = list()
games = list()

for c in soup.find_all('td'):
    if len(c.attrs) == 1:
        if '$' in c.get_text():
            prices.append(c.get_text())

for a in soup.find_all('a', {'class': 'b'}, rel=False):
    games.append(a.get_text()+' - '+'https://steamdb.info'+a.get('href'))

for line in zip(games,prices):
    file = open('steam_games.txt','a')
    file.write(str(line)+'\n')

file.close()