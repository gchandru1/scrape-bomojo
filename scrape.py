from bs4 import BeautifulSoup
from urllib2 import urlopen
import json
import csv

BASE_URL = "http://www.boxofficemojo.com"
FRANCHISE_URL = "/franchises/chart/?id=avengers.htm"

def get_soup(url):
    html = urlopen(BASE_URL + url).read()
    soup = BeautifulSoup(html, "lxml")
    return soup

def get_movie_links(soup):
    worldwide = soup.find(id="body").find_all("table")[2].find_all("table")[3]
    return [{"link" : link.get("href"),
             "title": link.text}
             for link in worldwide.find_all("a")]


def get_weekly_gross(soup, title):
    weekly_rows = soup.find("table", "chart-wide").find_all("tr")
    weekly_rows.pop(0)
    return [{"title": title,
             "date" : data.find_all("td")[0].text.replace(u"\x96", " - "),
             "gross": data.find_all("td")[2].text}
            for data in weekly_rows]

def get_all_weekly(soup):
    results = [get_weekly_gross(get_soup(data.get("link")+"&page=weekly"), data.get("title"))
                for data in get_movie_links(soup)]
    return [val for result in results for val in result]

def get_country_gross(soup, title):
    try:
        country_rows = soup.find(id="body").find_all("table")[4].find("table").find_all("tr")
        [country_rows.pop(0) for i in range(3)]
        return [{"title": title,
                 "country": data.find_all("td")[0].text,
                 "gross" : data.find_all("td")[5].text} 
                 for data in country_rows]
    except Exception, e:
        pass
    
def get_all_country(soup):
    results = [get_country_gross(get_soup(data.get("link")+"&page=intl"), data.get("title"))
                for data in get_movie_links(soup)]
    results = filter(None, results)
    return [val for result in results for val in result]
    
def save_json(flag):
    if flag == 0:
        json_data = json.dumps(get_all_weekly(get_soup(FRANCHISE_URL)))
    elif flag == 1:
        json_data = json.dumps(get_all_country(get_soup(FRANCHISE_URL)))
    f = open("data.json", "w+")
    f.write(json_data)
    f.close()
    print "Save to json file data.json"

if __name__ == "__main__":
    save_json(1)
