from bs4 import BeautifulSoup as bs
import requests 

poi = "LA BASILIQUE SAINT-SERNIN"
url = 'https://www.google.com/search?q='+poi
page = requests.get(url)
soup = bs(page.content, "lxml")