from bs4 import BeautifulSoup
import requests as r
import re

baseURL = "http://www.4crests.com/"
sitemapURL = "http://www.4crests.com/ind.html"
sitemapHTML = r.get(sitemapURL).text
sitemapSoup = BeautifulSoup(sitemapHTML, 'html.parser')
links = sitemapSoup.find_all('a', string=re.compile("'[A-Z]' surnames"))
links = [x.get("href") for x in links]

for link in links:
    pageURL = baseURL + link
    pageHTML = r.get(pageURL).text
    pageSoup = BeautifulSoup(pageHTML, 'html.parser')
    nameLinks = pageSoup.find_all('a', href=re.compile("[a-z]+-coat-of-arms.html"))
    nameLinks = [x.get("href") for x in nameLinks]
    
    for nameLink in nameLinks:
        pageURL = baseURL + link
        pageHTML = r.get(pageURL).text
        pageSoup = BeautifulSoup(pageHTML, 'html.parser')
        name = nameLink.split(".")[0]
        image = pageSoup.find('img', src=re.compile(name))
        try:
            image = image.get("src")
            print(image)
        
            with open("data\\" + name + ".gif", "wb") as f:
                response = r.get(image)
                f.write(response.content)
        
        except:
            print(name + ": Image not found!")
