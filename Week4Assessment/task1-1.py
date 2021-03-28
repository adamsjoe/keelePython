import sys
import csv
import datetime
from pprint import pprint

#reportDict = {}

# csv file names
BOOKLOANSFILE = 'bookloans.csv'
BOOKSFILE = 'books.csv'
REPORTFILETASK_1 = 'Task_1_report.csv'

def openFile(fileIn, skipHeader = False):
    """Open a file and returns the data.
    
        Wraps a basic file open in a function to allow this to be reused.  
        When I was examining the books and bookloans files I noticed that when reading the files, I always ended up with a very
        random "\ufeff1" appearing right at the begning of the data from the file.  Further examination with VS Code showed that the
        encoding of the file was "utf-8 with BOM" and that this random sequence was a symptom.  To corrrect this, the file had to be opened
        with "utf-8-sig" encoding.  I did consider if the encoding should also be made a parameter, but ultimately for these tasks kept this hard coded
        as both files share the same encoding.

        I also try to catch errors using a try/except block, I have one specific error "FileNotFoundError" and a generic catch all.  Error messages for
        both these occasions make use of string formatting to pass the fileIn parameter, which futher enhances re-usability.
        I fruther call sys.exit(1) which stops the execution and allows the OS to know there was a problem.

        I have checked the FileNotFound exception by passing in the name of a non-existing file.

        Keyword arguments:
            fileIn -- the file object whi chwill be opened
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

def convertEpochToReadable(dateIn):
    """Convert Excel Epoch time to a sting.

    This strange epoch format was a challenge for me.  In order to check if the date was in 2019 (which was asked for in the question) the only
    way I could think was to convert this format to something "human" readable and then check for the year.  This function simply takes in the epoch 
    date and passes out a human readable string.

    Note:
    Excel has a strange idea of epoch, as well a bug from Lotus notes, to convert the date to a readable format
    I used the following code, which was taken from the  Stackover Flow post referenced:
    
    https://stackoverflow.com/questions/14271791/converting-date-formats-python-unusual-date-formats-extract-ymd

    Before using this function, I tested this by taking the date columns in the bookloans.csv and converting them to "date" format.  
    I then checked that the dates returned by the function matched those of excel.  They did.

        Keyword arguments:
            dateIn -- the date (in excel epoch) format

        Returns:
            dateOut -- a date in string format (eg 12-01-1996)   
    """      
    # Mac and PC excel have different "start dates" - using a PC, but leaving the mac code in if needed.
    EXCEL_DATE_SYSTEM_PC=1900
    
    dateOut = datetime.date(EXCEL_DATE_SYSTEM_PC, 1, 1) + datetime.timedelta(dateIn-2)

    dateOut = dateOut.strftime("%d-%m-%Y")

    return dateOut

def containsDate(stringDate, dateToCheck):
    """Checks if a string contains another String.

    This takes two strings and returns a boolean if there is a substring match.  This is marked as "containsDate" but it is essentially a substring matching
    function and could be renamed and still not loose any readability or functionality.

        Keyword arguments:
            stringDate -- a date in string format, in truth this could be ANY string.
            dateToCheck -- a part of the date to check, in truth this could be any string.
    """
    # basic substring matching here.  If we find the substring, return True, else return False.
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

def sortAndGenerateTask1Content(dataIn):
    """
    For task 1 this converts the dictionary to a list and sorts at the same time.

    Keyword arguments:
    dataIn --  the dictionary which was built up in the buildTask1Details function.
    sorts on the field timesOutIn2019 and then converts this to a list for use with the CSV writer import.
    """
    reportOut = []
    print ("{:<12} {:<60} {:<40} {:<10}".format('Book Number','Title','Author','Times Loaned 2019'))
    for k, v in sorted(dataIn.items(), key=lambda e: e[1]["timesOut2019"]):
        item = [k, v['title'], v['author'], v['timesOut2019']]
        reportOut.append(item)
        print ("{:<12} {:<60} {:<40} {:<10}".format(k, v['title'], v['author'], v['timesOut2019']))
    return reportOut

def createReport(fileName, headers, content):
    """
    Creates a report file (currently a CSV)

    Keyword
    """
    try:
        with open(fileName, 'w', newline="") as outFile:
            csvwriter = csv.writer(outFile)
            csvwriter.writerow(headers)    
            csvwriter.writerows(content)
    except:
        print('Trying to create {} failed.  No further information was available'.format(fileName))
        sys.exit(1) 

# Task 1 specific code
reportHeaders = ['Book Number','Title','Author','Times Loaned 2019']
books = openFile(BOOKSFILE, False)
loans = openFile(BOOKLOANSFILE, False)
temp = buildTask1Details(loans)
contents = sortAndGenerateTask1Content(temp)
createReport(REPORTFILETASK_1, reportHeaders, contents)


