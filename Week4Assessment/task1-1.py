import csv
import datetime
from pprint import pprint

reportDict = {}

# csv file names
bookloansFile = 'bookloans.csv'
booksFile = 'books.csv'

def openFile(fileIn, skipHeader = False):
    """Open a file.
    
    Keyword arguments:
    fileIn -- the file object which will be opened
    skipHeader -- some files have "Headers" in the first row, if this is true we ignore these (defaults to False)
    """
    # setup a variable to hold the data from the file
    data = ''
    # myDictionary = {}
    try:
        with open(fileIn, encoding='utf-8-sig',mode='r') as file: # utf-8 with BOM results in \ufeff1 appearing
            reader = csv.reader(file)
            if skipHeader == True:
                next(reader, None)
            
            data = [tuple(row) for row in reader]
            # for row in reader:
            #     key = row[0]
            #     myDictionary[key] = row[1:]
    except FileNotFoundError: # handle file not found errors with a nice error message
        print('File {} does not exist.'.format(fileIn))
    except: # generic catch all error message
        print('Trying to open {} failed.  No further information was available'.format(fileIn))
    # return the data variable (the file contents)
    return data

def convertEpochToReadable(e):
    """
    Excel has a strange idea of epoch, as well a bug from Lotus notes, to convert the date to a readable format
    I used the following code, which was taken from the  stackoverflow post referenced:
    
    https://stackoverflow.com/questions/14271791/converting-date-formats-python-unusual-date-formats-extract-ymd
    
    This returns a XXXXXX
    """      
    EXCEL_DATE_SYSTEM_PC=1900
    d = datetime.date(EXCEL_DATE_SYSTEM_PC, 1, 1) + datetime.timedelta(e-2)
    d = d.strftime("%d-%m-%Y")
    return d

def containsDate(stringDate, dateToCheck):
    if dateToCheck in stringDate:
        return True
    else:
        return False

def max_value(inputlist):
    return max([sublist[-1] for sublist in inputlist])

def getval(x):
    global reportDict
    print(x)
    return reportDict[x]

def reportContent(loans):
    # reportDict = {}
    for row in loans:        
        # make things easier to find        
        bookNumber = row[0]
        bookNumber = int(bookNumber)
        loanedDateEpoch = row[2]
        loanedDateEpoch = int(loanedDateEpoch)
        LoanedDateReadable = convertEpochToReadable(loanedDateEpoch)
        

        # we will store the info on the books in a nested dictionary, first ensure book is not already present
        if bookNumber not in reportDict:
            reportDict[bookNumber] = {}

        if bookNumber in reportDict:
            # want to check if the date was in 2019, if so add it to a "loaned" count - not done yet
            if containsDate(LoanedDateReadable, '2019'):
                # no this is crap
                loanedTimes =  reportDict[bookNumber].get("timesOut2019")
                if loanedTimes is None: # check for none type cos you suck
                    loanedTimes = 1
                else:
                    loanedTimes += 1
            
            reportDict[bookNumber]["timesOut2019"] = loanedTimes
            bookFound = False
            
            for thing in books:
                bookRef = thing[0]
                if bookRef != 'Number':
                    bookRef = int(bookRef)
                if bookRef == bookNumber:
                    bookFound = True
            if bookFound:
                bookTitle = books[bookNumber][1]
                bookAuthor = books[bookNumber][2]       
            else:
                bookTitle = "No Title on file"
                bookAuthor = "No Author on file"
        else:
            # this is a new book
            reportDict[bookNumber]["timesOut2019"] = 1

        reportDict[bookNumber]["title"] = bookTitle
        reportDict[bookNumber]["author"] = bookAuthor
    # pprint(reportDict)
    print(reportDict[1]['timesOut2019'])
    return reportDict



books = openFile(booksFile, False)
loans = openFile(bookloansFile, False)

maxbooks = max_value(books)
temp = reportContent(loans)

uniqueSorted = sorted(temp, key = getval) # wtf?!?!?!