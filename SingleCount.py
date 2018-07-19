from bs4 import BeautifulSoup
import urllib.request as urllib2
from functions import get_text, NgramBuilder
import io
import operator


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
terms = {}
keywords = ""
department_frequency = {}
gridRows = 2
# Looping across all pages and getting links
for i in range (0, last_page_num):
    html_page = urllib2.urlopen("https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities?page=" + str(i+1) + "&lot=digital-specialists")
    soup = BeautifulSoup(html_page, "html5lib")
    # All the job titles are under a h2 heading, so getting all those links from the page
    for link in soup.select('h2 a[href]'):
        count +=1
        print("Count: " + str(count))
        # Removing the last useless link
        if ("//" not in link.get('href')):
            html_link = "https://www.digitalmarketplace.service.gov.uk" + link.get('href')

            # Get a list of most actively hiring departments
            html_sub_page = urllib2.urlopen(html_link)
            soup2 = BeautifulSoup(html_sub_page, "html5lib")
            if (len(soup2.find_all("div",class_="grid-row")[2].find("div").find_all("table")) > 0):
                gridRows = 2
                department = str(soup2.find_all("div",class_="grid-row")[2].find("div").find_all("table")[1].find("tbody").find_all("tr")[5].find_all("td")[1].find("span").contents[0])
            else:
                gridRows = 3
                department = str(soup2.find_all("div",class_="grid-row")[3].find("div").find_all("table")[1].find("tbody").find_all("tr")[5].find_all("td")[1].find("span").contents[0])

            print(department)
            if department not in department_frequency.keys():
                department_frequency[department] = 1
            else:
                department_frequency[department] += 1

            # Read contents of the job page

            page_text = get_text(html_link, gridRows)
            terms_in_link = NgramBuilder.ngramExtractor(NgramBuilder,page_text)
            no_of_keywords_in_link = len(terms_in_link)
            list_of_terms = list(terms_in_link)
            for j in range(0, no_of_keywords_in_link):
                if(list_of_terms[j][0] not in terms.keys()):
                    terms[list_of_terms[j][0]] = 1
                else:
                    terms[list_of_terms[j][0]] += 1

# Get ngram result in CSV format
resultList = sorted(terms.items(), key=operator.itemgetter(1), reverse=True)
result = ""
for j in range(0,len(resultList)):
    if(resultList[j][1] > 1):
        result += resultList[j][0] + "," + str(resultList[j][1]) + "\n"

# Get your department results in a CSV format
departmentResultsList = sorted(department_frequency.items(), key=operator.itemgetter(1), reverse=True)
departmentResult = ""
for j in range(0,len(departmentResultsList)):
    if(departmentResultsList[j][1] > 1):
        departmentResult += departmentResultsList[j][0] + "," + str(departmentResultsList[j][1]) + "\n"

# Store the master text in file
with io.open("Single_Count.csv", "w", encoding="utf-8") as f:
    f.write(result)
    f.close()

with io.open("Department_Frequency.csv", "w", encoding="utf-8") as f:
    f.write(departmentResult)
    f.close()