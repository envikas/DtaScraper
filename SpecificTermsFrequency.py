from bs4 import BeautifulSoup
import urllib.request as urllib2
from functions import get_text, NgramBuilder
import io
import operator

links = []

# Getting all pagination links
html_page = urllib2.urlopen("https://marketplace.service.gov.au/digital-marketplace/opportunities?page=1")
soup = BeautifulSoup(html_page, "html5lib")
# Getting the last page number
last_page_num = int(soup.find("div", class_="pagination").find("div").find_all("strong")[1].contents[0])

print("Number of pages:", last_page_num)

master_text = ""
count = 0
terms = {}
keywords = ""
department_frequency = {}
areas_of_expertise_frequency = {}
# Looping across all pages and getting links
for i in range(0, last_page_num):
    html_page = urllib2.urlopen(
        "https://marketplace.service.gov.au/digital-marketplace/opportunities?page=" + str(i + 1))
    soup = BeautifulSoup(html_page, "html5lib")
    # All the job titles are under a h2 heading, so getting all those links from the page
    for link in soup.select('h2 a[href]'):
        count += 1
        print(count)
        # Removing the last useless link
        if ("//" not in link.get('href')):
            html_link = "https://marketplace.service.gov.au" + link.get('href')

            # Get a list of most actively hiring departments
            html_sub_page = urllib2.urlopen(html_link)
            soup2 = BeautifulSoup(html_sub_page, "html5lib")
            department = str(
                soup2.find_all("div", class_="grid-row")[1].find("div").find_all("dl")[1].find_all("dd")[4].find(
                    "span").contents[0])
            area_of_expertise = str(
                soup2.find_all("div", class_="grid-row")[1].find("div").find_all("dl")[6].find_all("dd")[2].find(
                    "span").contents[0])
            area_of_expertise = "N/A" if area_of_expertise[0] is "<" else area_of_expertise
            # Getting active department frequencies
            if department not in department_frequency.keys():
                department_frequency[department] = 1
            else:
                department_frequency[department] += 1

            # Adding areas of expertise frequencies
            if area_of_expertise not in areas_of_expertise_frequency.keys():
                areas_of_expertise_frequency[area_of_expertise] = 1
            else:
                areas_of_expertise_frequency[area_of_expertise] += 1

            # Read contents of the job page

            page_text = get_text(html_link)
            terms_in_link = NgramBuilder.ngramExtractor(NgramBuilder, page_text)
            no_of_keywords_in_link = len(terms_in_link)
            list_of_terms = list(terms_in_link)
            for j in range(0, no_of_keywords_in_link):
                if (list_of_terms[j][0] not in terms.keys()):
                    terms[list_of_terms[j][0]] = 1
                else:
                    terms[list_of_terms[j][0]] += 1

required_terms = ["information","sharepoint","drupal","wordpress","automation","junior","senior","information technology","ict","agile","scrum","trello","jira","java","python","c","golang","cobol","manager","developer","baseline","security","citizen","citizenship","police verification","police check","baseline security clearance","testing","qa","teamwork","collaborate","collaborative","support","microsoft","office","presentation","permanent","contractor","contract","onsite","offsite","software","networks","networking","oracle","sql","database","databases","db","dba","oca","ocp","javascript","html","react","angular","remote","interpersonal","cyber","cybersecurity","cms","rfc","webpage","front end","back end","frontend","backend","front-end","back-end","australian citizenship","australian resident","permanent resident","salary","pay","payscale","australian capital territory","new south wales","act","nsw","victoria","queensland","northern territory","nt","south australia","sa","western australia","wa","tasmania","hobart","perth","sydney","melbourne","brisbane","adelaide","canberra","darwin","cairns","fortran","google","atlassian","git","github","vcs","version control","tortoise","bitbucket","regression testing","regression","performance","performance testing","dev tools","developer tools","visual studio","visual c++","visual c","android","ios","mobile","windows","net","dotnet","dot-net","c#","php","server","mainframe","django","perl","tomcat","apache","nosql","no-sql","relational database","relational databases","css","sass","business requirement","business requirements","vic","tas","apple","amazon","cloud","azure","web development","reactjs","react js","react native","angularjs","angular js","asp.net","api","compiler","devops","object oriented","functional","hadoop","heuristic","foxpro","fox","pharmcis","unity","unity3d","ai","machine learning","a.i.","neural network","qi","r","loadrunner","spring framework"]
# Get ngram result in CSV format
resultList = sorted(terms.items(), key=operator.itemgetter(1), reverse=True)
result = ""
for j in range(0, len(resultList)):
    if (resultList[j][1] > 1 and resultList[j][0] in required_terms):
        result += resultList[j][0] + "," + str(resultList[j][1]) + "\n"

# Get your department results in a CSV format
departmentResultsList = sorted(department_frequency.items(), key=operator.itemgetter(1), reverse=True)
departmentResult = ""
for j in range(0, len(departmentResultsList)):
    if (departmentResultsList[j][1] > 1):
        departmentResult += departmentResultsList[j][0] + "," + str(departmentResultsList[j][1]) + "\n"

# Getting areas of expertise in a CSV format
areasOfExpertiseResultsList = sorted(areas_of_expertise_frequency.items(), key=operator.itemgetter(1), reverse=True)
areasOfExpertiseResult = ""
for j in range(0, len(areasOfExpertiseResultsList)):
    if (areasOfExpertiseResultsList[j][1] > 1):
        areasOfExpertiseResult += areasOfExpertiseResultsList[j][0] + "," + str(areasOfExpertiseResultsList[j][1]) + "\n"

# Store the master text in file
with io.open("Single_Count.csv", "w", encoding="utf-8") as f:
    f.write(result)
    f.close()

with io.open("Department_Frequency.csv", "w", encoding="utf-8") as f:
    f.write(departmentResult)
    f.close()

with io.open("Areas_Of_Expertise.csv", "w", encoding="utf-8") as f:
    f.write(areasOfExpertiseResult)
    f.close()