import operator
import io

import functions

with open('Master_text.txt', 'r', encoding="utf-8") as myfile:
    text=myfile.read().replace('\n', '')

counter = functions.Counter()
builder = functions.NgramBuilder()
ngramLength = 3
# print("Finding N-Grams up to " + str(ngramLength) + " words")

for i in range (1 , ngramLength+1):
    counter.add(builder.find_ngrams(text, i))

resultList = sorted(counter.items(), key=operator.itemgetter(1), reverse=True)
result = ""

for j in range(0,len(resultList)):
    if(resultList[j][1] > 1):
        result += resultList[j][0] + "," + str(resultList[j][1]) + "\n"

print("Saving...")
with io.open("TermFrequencies.csv", "w", encoding="utf-8") as f:
    f.write(result)
    f.close()
