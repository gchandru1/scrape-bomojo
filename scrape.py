from bs4 import BeautifulSoup
from urllib2 import urlopen
import json

BASE_URL = "http://www.boxofficemojo.com"
FRANCHISE_URL = "/franchises/chart/?id=avengers.htm"

def get_movie_links(url):
    html = urlopen(BASE_URL + url).read()
    soup = BeautifulSoup(html, "lxml")
    worldwide = soup.find(id="body").find_all("table")[2].find_all("table")[3]
    return [{"link" : link.get("href"),
             "title": link.text}
             for link in worldwide.find_all("a")]


print json.dumps(get_movie_links(FRANCHISE_URL))
