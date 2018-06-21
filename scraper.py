from bs4 import BeautifulSoup
import urllib.request as urllib2
import re

links = []

# Getting all pagination links
html_page = urllib2.urlopen("https://marketplace.service.gov.au/digital-marketplace/opportunities?page=1")
soup = BeautifulSoup(html_page, "html5lib")
# Getting the last page number
last_page_num = int(soup.find("div", class_="pagination").find("div").find_all("strong")[1].contents[0])
print(last_page_num)

# Looping across all pages and getting links
for i in range (0, last_page_num):
    html_page = urllib2.urlopen("https://marketplace.service.gov.au/digital-marketplace/opportunities?page=" + str(i+1) )
    soup = BeautifulSoup(html_page, "html5lib")
    # All the job titles are under a h2 heading, so getting all those links from the page
    for link in soup.select('h2 a[href]'):
        links.append(link.get('href'))


print(links)