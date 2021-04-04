import sys
import csv
import datetime
from pprint import pprint

# csv file names
BOOKLOANSFILE = 'bookloans.csv'
BOOKSFILE = 'books.csv'
REPORTFILETASK_1 = 'Task_1_report.csv'
REPORTFILETASK_2 = 'Task_2_report.csv'
REPORTFILETASK_3 = 'Task_3_report.csv'

def openFile(fileIn, skipHeader = False):
    """
    Opens a CSV file and returns the data.
    
        Keyword arguments:
            fileIn -- the file object which will be opened
            skipHeader -- some files have "Headers" in the first row, if this is true we ignore these (defaults to False)

        Returns:
            data -- the object read from the file.
    """
    # setup a variable to hold the data from the file
    data = ''
    try:
        with open(fileIn, encoding='utf-8-sig',mode='r') as file: # utf-8 with BOM results in "\ufeff1" appearing
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

def convertEpochToReadable(dateIn):
    """
    Convert Excel Epoch time to a sting.

    Keyword arguments:
    dateIn -- the date (in excel epoch) format

    Returns:
    dateOut -- a date in string format (eg 12-01-1996)

    Note:
    Excel has a strange idea of epoch, as well a bug from Lotus notes, to convert the date to a readable format
    I used the following code, which was taken from the  Stackover Flow post referenced:
    
    https://stackoverflow.com/questions/14271791/converting-date-formats-python-unusual-date-formats-extract-ymd
    
    """      
    # Mac and PC excel have different "start dates" - using a PC, but leaving the mac code in if needed.
    EXCEL_DATE_SYSTEM_PC=1900
    EXCEL_DATE_SYSTEM_MAC=1904

    dateOut = datetime.date(EXCEL_DATE_SYSTEM_PC, 1, 1) + datetime.timedelta(dateIn-2)

    dateOut = dateOut.strftime("%d-%m-%Y")

    return dateOut

def containsDate(stringDate, dateToCheck):
    """
    Checks if a string contains another String.

    Keyword arguments:
    stringDate -- a date in string format, in truth this could be ANY string.
    dateToCheck -- a part of the date to check, in truth this could be any string.

    Notes:
    This is essentially a check to see if a substring exists inside a string.  However, being in a function makes it easier to read.
    """
    if dateToCheck in stringDate:
        return True
    else:
        return False

def buildTask1Details(loans):
    """
    Generate the content for the report.

    Keyword arguments:
    loans -- the list of data on the loans
    """
    reportDict = {}
    for row in loans:        
        # make things easier to reference
        bookNumber = row[0]
        bookNumber = int(bookNumber)        
        
        # get the loaned date, convert this to an int and convert to a readable string
        loanedDateEpoch = row[2]                
        loanedDateEpoch = int(loanedDateEpoch)
        LoanedDateReadable = convertEpochToReadable(loanedDateEpoch)
    
        # We will store the info on the books in a nested dictionary using the booknumber as a key.
        # First ensure the book is not already present:
        if bookNumber not in reportDict:
            reportDict[bookNumber] = {}

        if bookNumber in reportDict:
            # we need to check if the book which is being loaned is present in our cut down books.csv
            bookFound = False
            
            # loop through the books 
            for book in books:
                bookRef = book[0]
                if bookRef != 'Number': # bit sucky, to keep code working I had to bring in the headers.
                    bookRef = int(bookRef)
                if bookRef == bookNumber:
                    bookFound = True
            if bookFound:
                # we have found the book - so add the author and title to fields.
                bookTitle = books[bookNumber][1]
                bookAuthor = books[bookNumber][2]       
                if containsDate(LoanedDateReadable, '2019'):
                    # if the book was loanded in 2019, get the number of times this has been out.
                    loanedTimes =  reportDict[bookNumber].get("timesOut2019")
                    
                    # However, we may get a None type.  In this occasion, we can assume 
                    # the bookNumber isn't in the dictionary, so set the loanedTimes as 1
                    if loanedTimes is None: 
                        loanedTimes = 1
                    else:
                        loanedTimes += 1
            else:
                # if the book wasn't found, then we blank out the name and author
                bookTitle = ""
                bookAuthor = ""
            
        else:
            # this is a new book
            reportDict[bookNumber]["timesOut2019"] = 1

        # add to fields only if the bookTitle is not an empty string
        if bookTitle != "":
            # we write this to reportDict
            reportDict[bookNumber]["timesOut2019"] = loanedTimes
            reportDict[bookNumber]["title"] = bookTitle
            reportDict[bookNumber]["author"] = bookAuthor    
        else:
            # if the bookTitle is empty, then we also need to remove the booknumber from the final report
            reportDict.pop(bookNumber)
    
    return reportDict

def buildTask2Details(loans):
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

    Keyword arguments:
    fileName -- the name of the file we will be creating.
    headers -- the header row (columns) we need
    content -- a list containing the rows which will be included in the report
    """
    try:
        with open(fileName, 'w', newline="") as outFile:
            csvwriter = csv.writer(outFile)
            csvwriter.writerow(headers)    
            csvwriter.writerows(content)
    except:
        print('Trying to create {} failed.  No further information was available'.format(fileName))
        sys.exit(1) 

# load data in ready for working on
books = openFile(BOOKSFILE, False)
loans = openFile(BOOKLOANSFILE, False)

# Task 1 specific code
reportHeaders = ['Book Number','Title','Author','Times Loaned 2019']
# books = openFile(BOOKSFILE, False)
# loans = openFile(BOOKLOANSFILE, False)
temp = buildTask1Details(loans)
contents = sortAndGenerateTask1Content(temp, 1)
createReport(REPORTFILETASK_1, reportHeaders, contents)

# Task 2 specific code
# DOCUMENT ME MORE
reportHeaders = ['Genre','Count']
reportHeaders2 = ['Sub-Genre','Count']
temp = buildTask2Details(loans)

(a, b) = temp

genreReport = sortAndGenerateTask1Content(a, 2.1)
subGenreReport = sortAndGenerateTask1Content(b, 2.2)
createReport(REPORTFILETASK_2, reportHeaders, genreReport)
createReport(REPORTFILETASK_2, reportHeaders2, subGenreReport)