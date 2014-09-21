from bs4 import BeautifulSoup
from urllib2 import urlopen
import json

BASE_URL = "http://www.boxofficemojo.com"
FRANCHISE_URL = "/franchises/chart/?id=avengers.htm"

def get_soup(url):
    html = urlopen(BASE_URL + url).read()
    soup = BeautifulSoup(html, "lxml")
    return soup

def get_movie_links(soup):
    worldwide = soup.find(id="body").find_all("table")[2].find_all("table")[3]
    return [{"link" : link.get("href") + "&page=weekly",
             "title": link.text}
             for link in worldwide.find_all("a")]

def get_weekly_gross(soup):
    weekly_rows = soup.find("table", "chart-wide").find_all("tr")
    weekly_rows.pop(0)
    return [{"date" : data.find_all("td")[0].text,
             "gross": data.find_all("td")[2].text}
            for data in weekly_rows]

def get_all_weekly(soup):
    for data in get_movie_links(soup):
        url = data.get("link")
        title = data.get("title")
        print get_weekly_gross(get_soup(url))

print get_all_weekly(get_soup(FRANCHISE_URL))
