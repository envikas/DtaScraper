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
# Looping across all pages and getting links
for i in range (0, last_page_num):
    html_page = urllib2.urlopen("https://marketplace.service.gov.au/digital-marketplace/opportunities?page=" + str(i+1) )
    soup = BeautifulSoup(html_page, "html5lib")
    # All the job titles are under a h2 heading, so getting all those links from the page
    for link in soup.select('h2 a[href]'):
        count +=1
        print(count)
        # Removing the last useless link
        if ("//" not in link.get('href')):
            html_link = "https://marketplace.service.gov.au" + link.get('href')

            # Get a list of most actively hiring departments
            html_sub_page = urllib2.urlopen(html_link)
            soup2 = BeautifulSoup(html_sub_page, "html5lib")
            department = str(soup2.find_all("div",class_="grid-row")[1].find("div").find_all("dl")[1].find_all("dd")[4].find("span").contents[0])
            if department not in department_frequency.keys():
                department_frequency[department] = 1
            else:
                department_frequency[department] += 1

            # Read contents of the job page
            
            page_text = get_text(html_link)
            terms_in_link = NgramBuilder.ngramExtractor(NgramBuilder,page_text)
            no_of_keywords_in_link = len(terms_in_link)
            list_of_terms = list(terms_in_link)
            for j in range(0, no_of_keywords_in_link):
                if(list_of_terms[j][0] not in terms.keys()):
                    terms[list_of_terms[j][0]] = 1
                else:
                    terms[list_of_terms[j][0]] += 1

# Get ngram result in CSV format
required_terms = ["oracle", "windows", "windows server", "macos", "mac os", "osx" "os x", "unix", "sql server", "swift", "javascript", "machine learning", "sql", "mysql", "nosql", "hadoop", "cobol", "foxtran", "r", "matlab", "tensorflow", "php", "spring framework", "pharmcis", "qi", "angularjs", "no-sql", "mainframe", "jira", "trello", "automation", "artificial intelligence" , "data mining", "big data", "ibm", "watson", ".net", "dotnet", "git", "agile", "lean", "fox", "database", "cms", "wordpress", "drupal", "azure", "aws", "linux", "android", "ios", "java" ,"c", "c++", "c#", "python", "ruby", "scala", "django", "html", "css", "react", "reactjs", "reactnative", "angular"]
roles_terms = ["manager","business analyst", "engineer", "software engineer", "lawyer", "architect", "lead", "scrum master", "software developer", "programmer", "secretary"]
platform_terms = ["aws","linux","azure", "ibm","microsoft server", "unix"]
resultList = sorted(terms.items(), key=operator.itemgetter(1), reverse=True)
result = ""
roles_result = ""
platform_result =""

for j in range(0,len(resultList)):
    if(resultList[j][1] > 1 and resultList[j][0].lower() in required_terms):
        result += resultList[j][0] + "," + str(resultList[j][1]) + "\n"
    if (resultList[j][1] > 1 and resultList[j][0].lower() in roles_terms):
        roles_result += resultList[j][0] + "," + str(resultList[j][1]) + "\n"
    if (resultList[j][1] > 1 and resultList[j][0].lower() in platform_terms):
        platform_result += resultList[j][0] + "," + str(resultList[j][1]) + "\n"

# Get your department results in a CSV format
departmentResultsList = sorted(department_frequency.items(), key=operator.itemgetter(1), reverse=True)
departmentResult = ""
for j in range(0,len(departmentResultsList)):
    if(departmentResultsList[j][1] > 1):
        departmentResult += departmentResultsList[j][0] + "," + str(departmentResultsList[j][1]) + "\n"

# Store the master text in file
with io.open("Single_Count_aus.csv", "w", encoding="utf-8") as f:
    f.write(result)
    f.close()

with io.open("Roles_Count_aus.csv", "w", encoding="utf-8") as f:
    f.write(roles_result)
    f.close()

with io.open("Platform_Count_aus.csv", "w", encoding="utf-8") as f:
    f.write(platform_result)
    f.close()


with io.open("Department_Frequency_aus.csv", "w", encoding="utf-8") as f:
    f.write(departmentResult)
    f.close()