from BeautifulSoup import BeautifulSoup
from difflib import *
import zipfile, io, re, csv, sys

def main():
    country = raw_input("Enter a Country:")
    keyWord = getQuery() #raw_input("What would you like to know?")
    countrySearch(country, keyWord)

def countrySearch(country, key):
	file = open("countryList.txt", "r")
	countryCode= {}
	for line in file:
		# rline = re.sub("\s", " ", line).split()
		# print rline

	    if country in line:
	        page = line[:2] + ".html" #finds name of the country's file
	        break
	file.close()
	file = open("countryList.txt", "r")
	for line in file:
		countryCode[line[:2]] = line[3:].strip("\n").strip(' ')

	print page
	# for item in countryCode:
	# 	print item, countryCode[item]

	# print "-------", len(countryCode)

	archive = zipfile.ZipFile("countries.zip", "r") #access a zip archive

	for item in countryCode:
		pg = item + ".html"
		print pg
		file2 = archive.open(pg, "r")


		possibilities = parseHtml(file2)


		if key == ";lst":
			for key in possibilities.keys():
				print key + "," + possibilities[key]
			return

		if key == ";keys":
			for key in possibilities.keys():
				print key
			return

		results = get_close_matches(key, possibilities.keys())

		if key == ";matches":
			for result in results:
				print result
			return


		if(len(results) == 0): print "I'm afraid I can't do that."
		else:
			for result in results:
				print result + ": "
		print possibilities[result]

def parseHtml(htmlFile):
	soup = BeautifulSoup(htmlFile)

	possibilities = dict()

	for attr in soup.findAll("div", "category"):
		aTag = attr.find("a")
		if aTag:
			trTag = attr.parent.parent.findNextSibling("tr")

			if len(trTag) > 1:
				contents = []
				for div in trTag.findAll("div", "category"):
					if len(div.contents) > 0:
						contents.append(div.contents[0].strip())
						for span in div.find("span"):
							contents.append(span.string.strip())

				for div in trTag.findAll("div", "category_data"):
					if div.string:
						contents.append(div.string)

				data = "\r\n".join(contents)
			elif trTag.find("td"):
				data = trTag.find("td").find("div", "category_data").string
				print data
			else:
				data = trTag.find("div", "category_data").string

   		#alot of the titles contain extra info after a " - " which is throwing off the search
			title = formatKey(aTag.string)

			if possibilities.has_key(title):
				data = possibilities[title] + "\r\n" + data

			possibilities[title] = data

	return possibilities

def formatKey(key):
	words = key.split()

	temp = []
	for word in words:
		if word == "-":
			break
		else:
			temp.append(word)

	return " ".join(temp)


def getQuery():
	userInput = raw_input("What would you like to know?").lower()
	wordsToRemove = ["how", "what", "the", "a", "an", "which", "of", "in", ",", ":", ".", "?", "is"]

	words = []
	for word in userInput.split():
		if word not in wordsToRemove:
			words.append(word)

	userInput = " ".join(words)

	print userInput

	return userInput

def liveSuggestion(countryDetails):
    l = []
    c = []
    print "What kind of population Desnity do u prefer?\n1.High\n2.Low\n"
    b = int(raw_input())
    if(b == 1):
        l.append("high")
    elif(b == 2):
        l.append("low")
    else:
        print "Invalid selection"
        # continue
    print "What kind of Climate do u prefer?\n1.Cold\n2.Moderate\n3.Hot\n"
    c = int(raw_input())
    if(c == 1):
        l.append("cold")
    elif(c == 2):
        l.append("moderate")
    elif(c ==3):
        l.append("hot")
    else:
        print "Invalid selection"
        # continue
    print "What kind of Government do u prefer?\n1.Democracy\n2.Communist\n3.Monarchy\n4.Republic\n5.Federal"
    g = int(raw_input())
    if(g == 1):
        l.append("democracy")
    elif(g == 2):
        l.append("communist")
    elif(g ==3):
        l.append("monarchy")
    elif(g == 4):
        l.append("republic")
    elif(g ==5):
        l.append("federal")
    else:
        print "Invalid selection"
        # continue
    print "What is your religion?\n1.Christianity\n2.Buddhism\n3.Hinduism\n4.Islam\n5.Atheist"
    r = int(raw_input())
    if(r == 1):
        l.append("christianity")
    elif(r == 2):
        l.append("buddhism")
    elif(r ==3):
        l.append("hinduism")
    elif(r == 4):
        l.append("islam")
    elif(r ==5):
        l.append("athiest")
    else:
        print "Invalid selection"
        # continue
    # break

    possibleCountry = []
    for item in countryDetails:
        if countryDetails[item]["average weather"] == l[1] and countryDetails[item]["type of government"] == l[2] and countryDetails[item]["major religion"] == l[3]:
            possibleCountry.append(item)

    if possibleCountry != []:
        print "Your possible choices are: "
        for item in possibleCountry:
            print item
    else:
        print "Such a rare combination is not available among the top 30 rich countries of the world!"

def tourismSuggestion():
    tourism = {}
    placeList = []
    f = open("Tourism.csv")
    try:
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].lower()
            placeList.append(row)
    finally:
        f.close()

    l = len(placeList)
    for i in range(1, l):
        tourism[placeList[i][0]] = {}

    for i in range(1, l):
        for j in range(len(placeList[0])):
            if placeList[0][j] != "" and placeList[i][j] != "":
                tourism[placeList[i][0]][placeList[0][j]] = placeList[i][j]

    # for item in tourism:
    #     print item, "========"
    #     for domain in tourism[item]:
    #         print domain, '->', tourism[item][domain]


    l = []

    print "What is your total budget (per person) ?\n1. Under 1 lakh\n2. Between 1 and 2 lakhs\n3. Above 2 lakhs\n"

    c = int(raw_input())
    if(c == 1):
        l.append(0.5)
    elif(c == 2):
        l.append(1.5)
    elif(c ==3):
        l.append(2.5)

    print "What type of place do you wanna go?\n1. Historical Place\n2. Hill Station\n3. Desert Safari\n4. Beaches\n"

    p = int(raw_input())

    if(p == 1):
        l.append("historical")
    elif(p == 2):
        l.append("hill station")
    elif(p ==3):
        l.append("desert")
    elif(p == 4):
        l.append("beach")

    # print l
    # possiblePlaces = []
    print "The top 5 places you can visit are: "
    for item in tourism:
        # print item, '-----'
        # if tourism[item]["population density"] == l[0] and
        # print type(tourism[item]["budget"]), type(l[0])#, tourism[item]["type of place"], l[1]

        if float(tourism[item]["budget"]) == l[0] and tourism[item]["type of place"] == l[1]:
            print item.upper() + ",", tourism[item]["country"].upper()


def askQuestion(countryDetails):

    print "1. I want to migrate to another country. Please help me decide which country will be best suitable for me to live in.\n"
    print "2. I want to work in a country where I can earn most money. Where should I go?\n"
    print "3. I want to travel to exotic places in the world. Can you suggest me some?\n"

    a = int(raw_input())

    if(a == 1):
        liveSuggestion(countryDetails)

    elif(a == 2):
        # print "p2"
        x = int(raw_input('What is your work preference ? 1. a business  2. a job ? '))
        wp = False; #Work preference F: Business T: Job
        ie = False; #F: Import  T: Export
        fdomain = 0;
        jobtype = 0;    # 1: Startup 2: Local business 3: MNC

        if x == 1:
            wp = False;
            xa = int(raw_input('1.Imports or 2.Exports: '))
            print "Your field:"
            fdomain = int(raw_input('1. Technology,  2. Manufacturing,  3. Agriculture,  4. Infrastructure: '))
            # break;

        elif x == 2:
            wp = True;
            print "Your field:"
            fdomain = int(raw_input('1. Technology, 2. Manufacturing, 3. Agriculture, 4. Infrastructure: '))

            jobtype = int(raw_input('What type of company would you work for 1: Startup,  2: Local businesses,  3: MNC'))
            # break;
        else:
            print "wrong input"

    elif(a ==3):

        tourismSuggestion()

    else:
        print "Invalid option!"



def expertSystem():

    countryDetails = {}
    countryList = []
    f = open("countries.csv")
    try:
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].lower()
            countryList.append(row)
    finally:
        f.close()

	l = len(countryList)
	for i in range(1, l):
		countryDetails[countryList[i][0]] = {}

	for i in range(1, l):
		for j in range(len(countryList[0])):
			if countryList[0][j] != "" and countryList[i][j] != "":
				countryDetails[countryList[i][0]][countryList[0][j]] = countryList[i][j]

    # for item in countryDetails:
    # 	print item, '-----'
        # for domain in countryDetails[item]:
        # 	print domain#, '->', countryDetails[item][domain]
        # # print item, countryDetails[]

    askQuestion(countryDetails)








if __name__ == '__main__':

    print "Welcome to the Geographic Information Expert System!"
    print "\t1. Search about the geographic detais of any country in the world."
    print "\t2. Ask our Expert system suggestions to LIVE, WORK or TRAVEL in different countries.\n"

    choice = input()

    if choice == 1:
        main()

    elif choice == 2:
        expertSystem()

    else:
        "Invalid option. Please try again."
