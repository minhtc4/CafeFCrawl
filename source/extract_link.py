from bs4 import BeautifulSoup
import re
import json

soup = BeautifulSoup(open("../text").read(), 'lxml')
data = soup.findAll('a', attrs={'href': re.compile("^/equities/")})
stocks = {}
for i in data:
    stocks[i.get('href')] = i.text

with open('../stock.json', 'w') as f:
    json.dump(stocks, f)
