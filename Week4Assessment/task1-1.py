import csv
import datetime
from pprint import pprint

#reportDict = {}

# csv file names
bookloansFile = 'bookloans.csv'
booksFile = 'books.csv'
reportFile = 'Task_1_report.txt'

# this is wrong
def getval(x):
    global reportDict
    print(x)
    return reportDict[x]['timesOut2019']

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
    except: # generic catch all error message
        print('Trying to open {} failed.  No further information was available'.format(fileIn))
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

def reportContent(loans):
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
            # want to check if the date was in 2019, if so add it to a "loaned" count
            if containsDate(LoanedDateReadable, '2019'):
                # if the book was loanded in 2019, get the number of times this has been out.
                loanedTimes =  reportDict[bookNumber].get("timesOut2019")
                
                # However, we may get a None type.  In this occasion, we can assume 
                # the bookNumber isn't in the dictionary, so set the loanedTimes as 1
                if loanedTimes is None: 
                    loanedTimes = 1
                else:
                    loanedTimes += 1
            
            # Add the times loaned in 2019 to a field in the dictionary
            reportDict[bookNumber]["timesOut2019"] = loanedTimes

            # It seems that some books in the bookloans file don't exist in the books file, so we need to cover this.
            # We will use the bookFound flag in a search of the books data for the bookNumber used in the loans file.
            bookFound = False
            
            for thing in books:
                bookRef = thing[0]
                if bookRef != 'Number': # bit sucky, to keep code working I had to bring in the headers.
                    bookRef = int(bookRef)
                if bookRef == bookNumber:
                    bookFound = True
            if bookFound:
                # we have found the book - so add the author and title to fields.
                bookTitle = books[bookNumber][1]
                bookAuthor = books[bookNumber][2]       
            else:
                # We cannot disregarad - so we will use some placeholder data.
                bookTitle = "No Title on file"
                bookAuthor = "No Author on file"
        else:
            # this is a new book
            reportDict[bookNumber]["timesOut2019"] = 1

        # add to fields
        reportDict[bookNumber]["title"] = bookTitle
        reportDict[bookNumber]["author"] = bookAuthor    
    # print(reportDict[1]['timesOut2019'])
    return reportDict

def outputReport(contents, fileName):
    reportFile = open(fileName, 'a')
    reportFile.write("{:<12} {:<60} {:<40} {:<10}".format('Book Number','Title','Author','Times Loaned 2019'))
    for k, v in sorted(contents.items(), key=lambda e: e[1]["timesOut2019"]):
        reportFile.write("{:<12} {:<60} {:<40} {:<10}".format(k, v['title'], v['author'], v['timesOut2019']))

books = openFile(booksFile, False)
loans = openFile(bookloansFile, False)
temp = reportContent(loans)
#outputReport(temp, reportFile)


print ("{:<12} {:<60} {:<40} {:<10}".format('Book Number','Title','Author','Times Loaned 2019'))
for k, v in sorted(temp.items(), key=lambda e: e[1]["timesOut2019"]):
    #print(k, v)
    #print(v['timesOut2019'])    
    print ("{:<12} {:<60} {:<40} {:<10}".format(k, v['title'], v['author'], v['timesOut2019']))

#print(temp)



