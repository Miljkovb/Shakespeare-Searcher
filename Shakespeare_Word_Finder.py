from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from collections import defaultdict
from collections import Counter
from nltk.corpus import stopwords
import os
import json
import nltk
import re


"""url = "http://shakespeare.mit.edu/"""

def fetchFromURL(url):

    """

    Attempt to fetch content from URL via HTTP GET request. If it's HTML/XML return otherwise

    don't do anything

    """

    try:

        with closing(get(url, stream=True)) as resp:

            if is_good_response(resp):

                return resp.content

            else:

                return None

 

    except RequestException as e:

        log_error('Error during request to {0}:{1}' . format(url, str(e)))

        return None

 

def is_good_response(resp):

    """

    Returns True if response looks like HTML

    """

    content_type = resp.headers['Content-Type'].lower()

    return (resp.status_code == 200

            and content_type is not None

            and content_type.find('html') > -1)

 

def log_error(e):

    """

    log those errors or you'll regret it later...

    """

    print(e)

 

def get_target_urls(target):

    """

    Example of isolating different parent elements to gather subsequent URLs

    """
    webLinkList = []

    soup = BeautifulSoup(target, 'html.parser')

    for row in soup.find_all('td'):

        for link in row.find_all('a'):
            if 'http' not in link:
                webLinkList.append(link.get('href'))
    return webLinkList


def askUserInput():
    userInput = input("Please enter a term that you would like to search for. ")
    return userInput




def main():

    
    url = "http://shakespeare.mit.edu/"
    
    num = 1
    raw_html = fetchFromURL(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    
    linkList = get_target_urls(raw_html)
    finalLinkList = []
    newLinkList = []
   
    for link in linkList:
        if 'http' not in link:
            finalLinkList.append(link)
    """print(finalLinkList)"""



    allTerms = defaultdict(list)
    bigramdict = defaultdict(list)
    FullTermList = []

    dirName = "Full works"

    if not os.path.exists(dirName):
        os.mkdir(dirName)
    else:
        print("Directory " , dirName , "already exists")
        

    fullWorksDir = os.getcwd() + "/Full works"


    

    for link in finalLinkList:
       

            newDirName = "BiGram Index"
            if os.path.exists(newDirName):
                break
            
            url = "http://shakespeare.mit.edu/"
            url+= link
            
            subURL = fetchFromURL(url)
            textSoup = BeautifulSoup(subURL, 'html.parser')
            for rows in textSoup.find_all('p'):
                for links in rows.find_all('a'):
                    newfinalLinkList= []
                    newLinkList.append(links.get('href'))
                    
                    if 'full.html' in newLinkList:
                        newfinalLinkList.append('full.html')
            

            newLink = url.replace('index.html', 'full.html')
            fileName = url.replace('http://shakespeare.mit.edu/', '')
            fileName = fileName.replace('/index.html', '')
            fileName = fileName.replace('Poetry/', '')
            fileName = fileName.replace('.html', '')
            
            finalFetch = fetchFromURL(newLink)
            finalSoup = BeautifulSoup(finalFetch, 'html.parser')
            finalText = finalSoup.get_text()

            tokens = nltk.word_tokenize(finalText)



            
            """f = open(fileName , 'w+')"""

            wholeWorkFile = []
            dictionaryTXT = []
            """bigramdict = {}"""

            stopList = set(stopwords.words("english"))

            stopListSymbols = [".", ",", ":", "?", "!", "'s", "]", "[", "``", "''", "(",
                        ")", ";", "&", "$", "'", "-", "1", "2", "3", "4",
                        "5", "6", "7", "8", "9"]
            greatestFileName = "FullWork " +fileName

            completeName = os.path.join(fullWorksDir, greatestFileName)

            thisIsBroken = []
            
            f = open(completeName, 'w+')
            wholeWorkFile.append(finalText)
            for something in wholeWorkFile:
                if something not in stopList:
                    if something not in stopListSymbols:
                        f.write(something)
                            
                            
            f.close()

            


            for term in tokens:
                term = term.lower()
                if term not in stopList:
                    if term not in stopListSymbols:
                        if term not in thisIsBroken:
                            thisIsBroken.append(term)
                            FullTermList.append(term)
                        if fileName not in allTerms[term]:
                            allTerms[term].append(fileName)
            

            fullWordList = "TermList"
            thisThing = "fullTermListUntouched"
            

            ftl = open("fullTermListUntouched", 'w+')
            for hi in FullTermList:
                ftl.write(hi)
                ftl.write('\n')
                
            ftl.close()          


            
            for blank in tokens:
                blank = blank.lower()
                
                if blank not in stopList:
                    
                    if blank not in stopListSymbols:
                        
                        if blank not in dictionaryTXT:
                            newBlank = blank
                            
                            blank = "$" + blank + "$"
                            
                            dictionaryTXT.append(newBlank)
                            
                            n = 0
                            m = 2
                            checkValue = bigramdict[blank[0:2]]
                            if newBlank not in checkValue:
                                bigramdict[blank[0:2]].append(newBlank)
                            for letter in blank:
                                """print(letters)"""
                                checkVal = bigramdict[blank[n:m]]

                                if letter == '$':
                                    forget = ""
                                elif newBlank not in checkVal:
                                    bigramdict[blank[n:m]].append(newBlank)
                                """print(bigramdict)"""
                                n = n + 1
                                m = m + 1
        
                
                
    
   
   
    
    with open("BiGram Index" + ".json", 'w+') as fp:
        json.dump(bigramdict, fp, sort_keys = True, indent = 4)



    with open("fullTermListUntouched") as pn:
        wordCount = Counter(pn.read().split())


    for term in allTerms:
        allTerms[term].insert(0,wordCount[term])

    with open("TermListCounted" + ".json", 'w+') as tl:
        json.dump(allTerms, tl, sort_keys = True, indent = 4)
        
        
        
    workCount = "WordCount"
        


    with open(workCount + ".json", 'w+') as wc:
        json.dump(wordCount, wc, sort_keys = True, indent = 4)


    while True:
        searchInput = input("Would you like to search a word? (y/n)")
        if searchInput == "n":
            break
        elif searchInput == "y":
            userInput = input("Please enter a term that you would like to search for. ")


            if userInput in allTerms:
                allTerms.get(userInput)
                print(allTerms.get(userInput))
                print("it worked")

            else:
                print("Did you mean? ")
                for term in allTerms:
                    jd = nltk.jaccard_distance(set(userInput), set(term))
                    if jd < .3:
                        print(term)
                
             
    
        
main()


        



 
