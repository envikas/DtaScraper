from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
from functions import get_text
import io


links = []

# Getting all pagination links
html_page = urllib2.urlopen("https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities?page=1&lot=digital-specialists")
soup = BeautifulSoup(html_page, "html5lib")
# Getting the last page number
page_num = soup.find("span", class_="page-numbers").contents
last_page_num = int(page_num[0][-2:])
print("Number of pages:", last_page_num)

master_text = ""
count = 0
# Looping across all pages and getting links
for i in range (0, last_page_num):
    html_page = urllib2.urlopen("https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities?page=" + str(i+1) + "&lot=digital-specialists")
    soup = BeautifulSoup(html_page, "html5lib")
    # All the job titles are under a h2 heading, so getting all those links from the page
    for link in soup.select('h2 a[href]'):
        count +=1
        print(count)
        # Removing the last useless link
        if ("//" not in link.get('href')):
            html_link = "https://marketplace.service.gov.au" + link.get('href')
            page_text = get_text(html_link)
            master_text += page_text
            links.append(html_link)


# Store the master text in file
with io.open("Master_text.txt", "w", encoding="utf-8") as f:
    f.write(master_text)
    f.close()