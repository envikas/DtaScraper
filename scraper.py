from bs4 import BeautifulSoup
import urllib.request as urllib2
import re

# Getting all pagination links
html_page = urllib2.urlopen("https://marketplace.service.gov.au/digital-marketplace/opportunities?page=1")
soup = BeautifulSoup(html_page, "html5lib")
links = []

# All the job titles are under a h2 heading, so getting all those links from the page
for link in soup.select('h2 a[href]'):
    links.append(link.get('href'))

print(links)