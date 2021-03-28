import sys
import csv
from pprint import pprint

#reportDict = {}

# csv file names
bookloansFile = 'bookloans.csv'
booksFile = 'books.csv'
reportFileTask1 = 'Task_1_report.csv'
reportFileTask2 = 'Task_2_report.csv'
reportFileTask3 = 'Task_3_report.csv'


def openFile(fileIn, skipHeader = False):
    """Open a file.
    
    Keyword arguments:
    fileIn -- the file object which will be opened
    skipHeader -- some files have "Headers" in the first row, if this is true we ignore these (defaults to False)

    Returns:
    data -- the object read from the file.
    """
    # setup a variable to hold the data from the file
    data = ''
    try:
        with open(fileIn, encoding='utf-8-sig',mode='r') as file: # utf-8 with BOM results in \ufeff1 appearing
            reader = csv.reader(file)
            if skipHeader == True:
                next(reader, None)
            
            data = [tuple(row) for row in reader]
    except FileNotFoundError: # handle file not found errors with a nice error message
        print('File {} does not exist.'.format(fileIn))
        sys.exit(1)
    except: # generic catch all error message
        print('Trying to open {} failed.  No further information was available'.format(fileIn))
        sys.exit(1)
    # return the data variable (the file contents)
    return data

def buildTask1Details(loans):
    """
    Generate the content for the report.

    Keyword arguments:
    loans -- the list of data on the loans
    """
    reportDict = {}
    genreDict = {}
    subGenreDict = {}
    genreCount = 0
    subGenreCount = 0    
    for row in loans:        
        # get the booknumber from the bookloans list
        bookNumber = row[0]
        bookNumber = int(bookNumber)
        genre = ""#books[bookNumber][3]
        subGenre = ""#books[bookNumber][4]       
        
        for book in books:
            bookRef = book[0]
            if bookRef != 'Number': # bit sucky, to keep code working I had to bring in the headers.
                bookRef = int(bookRef)
                if bookRef == bookNumber:
                    bookFound = True
                    genre = books[bookNumber][3]
                    subGenre = books[bookNumber][4]     
                    break
        if bookFound:
            # here we cycle through the loans and update counters in 2 dictionaries depending on the genre and subgenre
            if genre not in genreDict:
                if genre != "":
                    genreDict[genre] = {}
                    genreCount = 0
                    genreDict[genre] = 1        
            else:
                genreCount = genreDict[genre]
                genreCount = int(genreCount) # not needed as we control this 
                genreCount += 1
                genreDict[genre] = genreCount
      
            if subGenre not in subGenreDict:
                if subGenre != "":
                    subGenreDict[subGenre] = {}
                    subGenreCount = 0
                    subGenreDict[subGenre] = 1
            else:
                subGenreCount = subGenreDict[subGenre]
                subGenreCount = int(subGenreCount)
                subGenreCount += 1
                subGenreDict[subGenre] = subGenreCount
    
        reportDict = tuple([genreDict, subGenreDict])
        #we could do this based off genre, each genre can have multiple sub genres
      
    return reportDict

def sortAndGenerateTask1Content(dataIn, taskNum):
    """
    For task 1 this converts the dictionary to a list and sorts at the same time.

    Keyword arguments:
    dataIn --  the dictionary which was built up in the buildTask1Details function.
    sorts on the field timesOutIn2019 and then converts this to a list for use with the CSV writer import.
    """
    reportOut = []
    if taskNum == 1:
        print ("{:<12} {:<60} {:<40} {:<10}".format('Book Number','Title','Author','Times Loaned 2019'))
        for k, v in sorted(dataIn.items(), key=lambda e: e[1]["timesOut2019"]):
            item = [k, v['title'], v['author'], v['timesOut2019']]
            reportOut.append(item)
            print ("{:<12} {:<60} {:<40} {:<10}".format(k, v['title'], v['author'], v['timesOut2019']))
        return reportOut
    elif taskNum == 2.1:
        print ("{:<20} {:<10}".format('Genre','Count'))
        for k,v in dataIn.items():
            item = [k, v]
            reportOut.append(item)
            print ("{:<20} {:<10}".format(k,v))
        return reportOut
    elif taskNum == 2.2:
        print ("{:<20} {:<10}".format('Sub-Genre','Count'))
        for k,v in dataIn.items():
            item = [k, v]
            reportOut.append(item)
            print ("{:<20} {:<10}".format(k,v))
        return reportOut    
    else:
        print("incorrect task number.  please try again")
        sys.exit(1)

def createReport(fileName, headers, content):
    """
    Creates a report file (currently a CSV)

    Keyword
    """
    try:
        with open(fileName, 'a', newline="") as outFile:
            csvwriter = csv.writer(outFile)
            csvwriter.writerow(headers)    
            csvwriter.writerows(content)
    except:
        print('Trying to create {} failed.  No further information was available'.format(fileName))
        sys.exit(1) 

books = openFile(booksFile)
loans = openFile(bookloansFile)
temp = buildTask1Details(loans)

# temp is a tubpe of two lists, we can split them int
(genreList, subGenreList) = temp

reportHeaders = ['Genre','Count']
reportHeaders2 = ['Sub-Genre','Count']
blah = sortAndGenerateTask1Content(genreList, 2.1)
blah2 = sortAndGenerateTask1Content(subGenreList, 2.2)
createReport(reportFileTask2, reportHeaders, blah)
createReport(reportFileTask2, reportHeaders2, blah2)

# contents = sortAndGenerateTask1Content(temp)


