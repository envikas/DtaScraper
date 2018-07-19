from bs4 import BeautifulSoup
import urllib.request as urllib2
import operator

def get_text(link, gridRows):
    text = ""
    html_page = urllib2.urlopen(link)
    soup = BeautifulSoup(html_page, "html5lib")
    # Getting essential skills and experience
    # Checking if the skills list is empty
    if not soup.find_all("div",class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find("tr").find_all("td")[1].find("span"):
        text += "NA"
    # Checking if the skills are in a list or not
    elif (soup.find_all("div",class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find("tr").find_all("td")[1].find("span").find("ul")):
        num_of_grid_rows = len(soup.find_all("div",class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find("tr").find_all("td")[1].find("span").find("ul").find_all("li"))
        for i in range(0, num_of_grid_rows):
            text += soup.find_all("div",class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find("tr").find_all("td")[1].find("span").find("ul").find_all("li")[i].get_text()
    # No list, just a span, then do this:
    else:
        text += soup.find_all("div", class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find(
            "tr").find_all("td")[1].find("span").get_text()

    # Getting nice-to-have skills and experience
    # Checking if the skills list is empty
    if not soup.find_all("div", class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find_all(
            "tr")[1].find_all("td")[1].find("span"):
        text += "NA"
        return text
    # Checking if the skills are in a list or not
    elif (soup.find_all("div", class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find_all(
            "tr")[1].find_all("td")[1].find("span").find("ul")):
        num_of_grid_rows = len(
            soup.find_all("div", class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find_all(
                "tr")[1].find_all("td")[1].find("span").find("ul").find_all("li"))
        for i in range(0, num_of_grid_rows):
            text += \
            soup.find_all("div", class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find_all(
                "tr")[1].find_all("td")[1].find("span").find("ul").find_all("li")[i].get_text()
        return text
    # No list, just a span, then do this:
    else:
        text += soup.find_all("div", class_="grid-row")[gridRows].find("div").find_all("table")[5].find("tbody").find_all(
            "tr")[1].find_all("td")[1].find("span").get_text()
        return text




# Test of get_text
# print(get_text("https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/7119", 3))


import re

import nltk.tokenize

__version__ = "0.1.0"


class Counter(dict):
    def add(self, other):
        for ngram in other.keys():
            self[ngram] = self.get(ngram, 0) + other[ngram]

    def remove_subphrases(self):
        builder = NgramBuilder()
        to_remove = {}
        for phrase in self.keys():
            for length in range(1, len(phrase.split(" "))):
                for subphrase in builder.find_ngrams(phrase, length).keys():
                    if subphrase in self and self[subphrase] == self[phrase]:
                        to_remove[subphrase] = 1
        for subphrase in to_remove.keys():
            del self[subphrase]


class NgramBuilder(object):
    def __init__(self):
        self.stopwords = stopwords

    def find_ngrams(self, text, length):
        counter = Counter()
        num_unigrams, unigrams = self.split_into_unigrams(text.lower())
        for i in range(num_unigrams):
            if (num_unigrams <= i + length - 1):
                break
            unigram_group = unigrams[i:i + length]
            if not self.ngram_is_filtered(unigram_group):
                ngram = " ".join(unigram_group)
                counter[ngram] = counter.get(ngram, 0) + 1
        return counter

    def split_into_unigrams(self, text):
        unigrams = []
        for token in nltk.tokenize.WhitespaceTokenizer().tokenize(text):
            unigram = self.token_to_unigram(token)
            if unigram:
                unigrams.append(unigram)
        return len(unigrams), unigrams

    def token_to_unigram(self, token):
        token = token.strip().strip(",.!|&-_()[]<>?{}/\"'").strip()

        def has_no_chars(token):
            for char in token:
                if char.isalpha():
                    return False
            return True

        if len(token) == 1 or token.isdigit() or has_no_chars(token):
            return None
        return token

    def ngram_starts_or_ends_in_stopword(self, unigrams):
        if self.stopwords is None:
            return False
        return unigrams[0].lower() in self.stopwords or unigrams[-1].lower() in self.stopwords


    def ngram_is_filtered(self, unigrams):
        return self.ngram_starts_or_ends_in_stopword(unigrams)

    def ngramExtractor(self, text):
        counter = Counter()
        builder = NgramBuilder()
        ngramLength = 3
        # print("Finding N-Grams up to " + str(ngramLength) + " words")

        for i in range(1, ngramLength + 1):
            counter.add(builder.find_ngrams(text, i))

        return counter.items()



stopwords = set(["published","deadline","applications","write","summary","start","contract","meet","street","identify","5pm","specialist","relevant","setup","arrangements","conditions","months","key","approach","ensure","payment","interview","minimum","include","skills","sellersâ€™","buyer","seller","day","question","answer","provide","week","days","buyers","buyers","evaluate","sellers","evaluated","summary","cultural","dates","id","essential","date","nice-to-have","opportunity", "clearance","terms","competence","price","seller","questions","additional","closing","overview","6pm","required","role?","do?","day?","specialists?","evaluate?",
                 """a""","""able""","""about""","""above""","""abroad""","""according""","""accordingly""","""across""","""actually""","""adj""","""after""","""afterwards""","""again""","""against""","""ago""","""ahead""","""ain't""","""all""","""allow""","""allows""","""almost""","""alone""","""along""","""alongside""","""already""","""also""","""although""","""always""","""am""","""amid""","""amidst""","""among""","""amongst""","""an""","""and""","""another""","""any""","""anybody""","""anyhow""","""anyone""","""anything""","""anyway""","""anyways""","""anywhere""","""apart""","""appear""","""appreciate""","""appropriate""","""are""","area","areas","""aren't""","""around""","""as""","""a's""","""aside""","""ask""","asked","""asking""","asks","""associated""","""at""","""available""","""away""","""awfully""","""b""","""back""","backed","backing","backs","""backward""","""backwards""","""be""","""became""","""because""","""become""","""becomes""","""becoming""","""been""","""before""","""beforehand""","began","""begin""","""behind""","""being""","beings","""believe""","""below""","""beside""","""besides""","""best""","""better""","""between""","""beyond""","big","""both""","""brief""","""but""","""by""","""c""","""came""","""can""","""cannot""","""cant""","""can't""","""caption""","case","cases","""cause""","""causes""","""certain""","""certainly""","""changes""","clear","""clearly""","""c'mon""","""co""","""co.""","""com""","""come""","""comes""","""concerning""","""consequently""","""consider""","""considering""","""contain""","""containing""","""contains""","""corresponding""","""could""","""couldn't""","""course""","""c's""","""currently""","""d""","""dare""","""daren't""","""definitely""","""described""","""despite""","""did""","""didn't""","differ","""different""","differently","""directly""","""do""","""does""","""doesn't""","""doing""","""done""","""don't""","""down""","downed","downing","downs","""downwards""","""during""","""e""","""each""","early","""edu""","""eg""","""eight""","""eighty""","""either""","""else""","""elsewhere""","""end""","ended","""ending""","ends","""enough""","""entirely""","""especially""","""et""","""etc""","""even""","evenly","""ever""","""evermore""","""every""","""everybody""","""everyone""","""everything""","""everywhere""","""ex""","""exactly""","""example""","""except""","""f""","face","faces","fact","facts","""fairly""","""far""","""farther""","felt","""few""","""fewer""","""fifth""","find","finds","""first""","""five""","""followed""","""following""","""follows""","""for""","""forever""","""former""","""formerly""","""forth""","""forward""","""found""","""four""","""from""","full","fully","""further""","furthered","furthering","""furthermore""","furthers","""g""","gave","general","generally","""get""","""gets""","""getting""","give","""given""","""gives""","""go""","""goes""","""going""","""gone""","good","goods","""got""","""gotten""","great","greater","greatest","""greetings""","group","grouped","grouping","groups","""h""","""had""","""hadn't""","""half""","""happens""","""hardly""","""has""","""hasn't""","""have""","""haven't""","""having""","""he""","""he'd""","""he'll""","""hello""","""help""","""hence""","""her""","""here""","""hereafter""","""hereby""","""herein""","""here's""","""hereupon""","""hers""","""herself""","""he's""","""hi""","high","higher","highest","""him""","""himself""","""his""","""hither""","""hopefully""","""how""","""howbeit""","""however""","""hundred""","""i""","""i'd""","""ie""","""if""","""ignored""","""i'll""","""i'm""","""immediate""","important","""in""","""inasmuch""","""inc""","""inc.""","""indeed""","""indicate""","""indicated""","""indicates""","""inner""","""inside""","""insofar""","""instead""","interest","interested","interesting","interests","""into""","""inward""","""is""","""isn't""","""it""","""it'd""","""it'll""","""its""","""it's""","""itself""","""i've""","""j""","""just""","""k""","""keep""","""keeps""","""kept""","kind","knew","""know""","""known""","""knows""","""l""","large","largely","""last""","""lately""","""later""","latest","""latter""","""latterly""","""least""","""less""","""lest""","""let""","lets","""let's""","""like""","""liked""","""likely""","""likewise""","""little""","long","longer","longest","""look""","""looking""","""looks""","""low""","""lower""","""ltd""","""m""","""made""","""mainly""","""make""","""makes""","making","man","""many""","""may""","""maybe""","""mayn't""","""me""","""mean""","""meantime""","""meanwhile""","member","members","men","""merely""","""might""","""mightn't""","""mine""","""minus""","""miss""","""more""","""moreover""","""most""","""mostly""","""mr""","""mrs""","""much""","""must""","""mustn't""","""my""","""myself""","""n""","""name""","""namely""","""nd""","""near""","""nearly""","""necessary""","""need""","needed","needing","""needn't""","""needs""","""neither""","""never""","""neverf""","""neverless""","""nevertheless""","newer","newest","""next""","""nine""","""ninety""","""no""","""nobody""","""non""","""none""","""nonetheless""","""noone""","""no-one""","""nor""","""normally""","""not""","""nothing""","""notwithstanding""","""novel""","""now""","""nowhere""","number","numbers","""o""","""obviously""","""of""","""off""","""often""","""oh""","""ok""","""okay""","""old""","older","oldest","""on""","""once""","""one""","""ones""","""one's""","""only""","""onto""","open","opened","opening","opens","""opposite""","""or""","order","ordered","ordering","orders","""other""","""others""","""otherwise""","""ought""","""oughtn't""","""our""","""ours""","""ourselves""","""out""","""outside""","""over""","""overall""","""own""","""p""","part","parted","""particular""","""particularly""","parting","parts","""past""","""per""","""perhaps""","place","""placed""","places","""please""","""plus""","point","pointed","pointing","points","""possible""","present","presented","presenting","presents","""presumably""","""probably""","problem","problems","""provided""","""provides""","put","puts","""q""","""que""","""quite""","""qv""","""r""","""rather""","""rd""","""re""","""really""","""reasonably""","""recent""","""recently""","""regarding""","""regardless""","""regards""","""relatively""","""respectively""","""right""","room","rooms","""round""","""s""","""said""","""same""","""saw""","""say""","""saying""","""says""","""second""","""secondly""","seconds","""see""","""seeing""","""seem""","""seemed""","""seeming""","""seems""","""seen""","sees","""self""","""selves""","""sensible""","""sent""","""serious""","""seriously""","""seven""","""several""","""shall""","""shan't""","""she""","""she'd""","""she'll""","""she's""","""should""","""shouldn't""","show","showed","showing","shows","side","sides","""since""","""six""","small","smaller","smallest","""so""","""some""","""somebody""","""someday""","""somehow""","""someone""","""something""","""sometime""","""sometimes""","""somewhat""","""somewhere""","""soon""","""sorry""","""specified""","""specify""","""specifying""","state","states","""still""","""sub""","""such""","""sup""","""sure""","""t""","""take""","""taken""","""taking""","""tell""","""tends""","""th""","""than""","""thank""","""thanks""","""thanx""","""that""","""that'll""","""thats""","""that's""","""that've""","""the""","""their""","""theirs""","""them""","""themselves""","""then""","""thence""","""there""","""thereafter""","""thereby""","""there'd""","""therefore""","""therein""","""there'll""","""there're""","""theres""","""there's""","""thereupon""","""there've""","""these""","""they""","""they'd""","""they'll""","""they're""","""they've""","""thing""","""things""","""think""","thinks","""third""","""thirty""","""this""","""thorough""","""thoroughly""","""those""","""though""","thought","thoughts","""three""","""through""","""throughout""","""thru""","""thus""","""till""","""to""","today","""together""","""too""","""took""","""toward""","""towards""","""tried""","""tries""","""truly""","""try""","""trying""","""t's""","turn","turned","turning","turns","""twice""","""two""","""u""","""un""","""under""","""underneath""","""undoing""","""unfortunately""","""unless""","""unlike""","""unlikely""","""until""","""unto""","""up""","""upon""","""upwards""","""us""","""use""","""used""","""useful""","""uses""","""using""","""usually""","""v""","""value""","""various""","""versus""","""very""","""via""","""viz""","""vs""","""w""","""want""","wanted","wanting","""wants""","""was""","""wasn't""","""way""","ways","""we""","""we'd""","""welcome""","""well""","""we'll""","wells","""went""","""were""","""we're""","""weren't""","""we've""","""what""","""whatever""","""what'll""","""what's""","""what've""","""when""","""whence""","""whenever""","""where""","""whereafter""","""whereas""","""whereby""","""wherein""","""where's""","""whereupon""","""wherever""","""whether""","""which""","""whichever""","""while""","""whilst""","""whither""","""who""","""who'd""","""whoever""","""whole""","""who'll""","""whom""","""whomever""","""who's""","""whose""","""why""","""will""","""willing""","""wish""","""with""","""within""","""without""","""wonder""","""won't""","work","worked","working","works","""would""","""wouldn't""","""x""","""y""","year","years","""yes""","""yet""","""you""","""you'd""","""you'll""","young","younger","youngest","""your""","""you're""","""yours""","""yourself""","""yourselves""","""you've""","""z""","""zero"""]
)