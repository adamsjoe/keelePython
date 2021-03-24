import csv
import datetime
from pprint import pprint

# csv file names
bookloansFile = 'bookloans.csv'
booksFile = 'books.csv'

def openFile(fileIn, skipHeader = False):
    data = ''
    # myDictionary = {}
    try:
        with open(fileIn, encoding='utf-8-sig',mode='r') as file: # utf-8 with BOM results in \ufeff1 appearing
            reader = csv.reader(file)
            if skipHeader == True:
                next(reader, None)
            #
            data = [tuple(row) for row in reader]
            # for row in reader:
            #     key = row[0]
            #     myDictionary[key] = row[1:]
    except FileNotFoundError:
        print('File {} does not exist.'.format(fileIn))
    except:
        print('Trying to open {} failed.  No further information was available'.format(fileIn))
    return data

def convertEpochToReadable(e):
    # https://stackoverflow.com/questions/14271791/converting-date-formats-python-unusual-date-formats-extract-ymd
   
    EXCEL_DATE_SYSTEM_PC=1900
    d = datetime.date(EXCEL_DATE_SYSTEM_PC, 1, 1) + datetime.timedelta(e-2)
    return d

def containsDate(stringDate, dateToCheck):
    if dateToCheck in stringDate:
        return True
    else:
        return False

def reportContent(loans, books):
    reportDict = {}
    for row in loans:        
        # make things easier to find        
        bookNumber = row[0]
        bookNumber = int(bookNumber)
        loanedDateEpoch = row[2]
        loanedDateEpoch = int(loanedDateEpoch)
        # LoaedDateReadable = convertEpochToReadable(loanedDateEpoch)

        # we will store the info on the books in a nested dictionary, first ensure it is not already present
        if bookNumber not in reportDict:
            reportDict[bookNumber] = {}
        

        if bookNumber in reportDict:
            # want to check if the date was in 2019, if so add it to a "loaned" count - not done yet
            
            # no this is crap
            loanedTimes =  reportDict[bookNumber].get("timesOut2019")
            if loanedTimes is None: # check for none type cos you suck
                loanedTimes = 1
            else:
                loanedTimes += 1
            
            reportDict[bookNumber]["timesOut2019"] = loanedTimes
            # reportDict[bookNumber]["title"] = books[bookNumber-1][1]
            # reportDict[bookNumber]["author"] = books[bookNumber-1][2]
        else:
            # this is a new book
            reportDict[bookNumber]["timesOut2019"] = 1
            # reportDict[bookNumber]["title"] = books[bookNumber-1][1]
            # reportDict[bookNumber]["author"] = books[bookNumber-1][2]
        reportDict[bookNumber]["title"] = books[bookNumber-1][1]
        reportDict[bookNumber]["author"] = books[bookNumber-1][2]

    pprint(reportDict)

books = openFile(booksFile, True)
loans = openFile(bookloansFile, False)
reportContent(loans, books)

#pprint(books)
#pprint(loans)
