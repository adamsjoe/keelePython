import sys
import csv
import datetime
from pprint import pprint

#reportDict = {}

# csv file names
bookloansFile = 'bookloans.csv'
booksFile = 'books.csv'
reportFileTask1 = 'Task_1_report.csv'
reportFileTask2 = 'Task_2_report.csv'
reportFileTask3 = 'Task_3_report.csv'
loanPeriod = 14

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

def buildTask3Details(loans):
    """
    Generate the content for the report.

    Keyword arguments:
    loans -- the list of data on the loans
    """
    reportDict = {}
    noOfUsers = 0
    noOfUsersLate = 0 
    totalDaysLate = 0
    users = set()
    usersLate = set()
    
    print ("{:<15} {:<10} {:<20} {:<20} {:<20}".format('book','member', 'start date', 'end date', 'days loaned'))
    for row in loans:        
        # get the booknumber from the bookloans list
        bookNumber = row[0]
        bookNumber = int(bookNumber)
        member = row[1]        
        loanStart = int(row[2])
        loanEnd = int(row[3])
        loanStartReadable = convertEpochToReadable(loanStart)        
        loanEndReadable = ""
        loanStatus = ""
        


        daysLate = 0 
        loanLen = 0        
        if loanEnd != 0:
            loanEndReadable = convertEpochToReadable(loanEnd)
            loanLen = loanEnd - loanStart
        else:
            loanEndReadable = "Item on loan"

        # be a smart ass and work out if the books on loan are overdue based on now date?
        if loanLen > 14:
            loanStatus = "Was Late"
            if member not in usersLate:
                usersLate.add(member)
            daysLate = loanLen - 14
            totalDaysLate =+ daysLate
        elif loanEnd != 0 and loanLen <=14:
            loanStatus = "Returned on time"        
        
        if member not in users:
            users.add(member)

        print("{:<15} {:<10} {:<20} {:<20} {:<20} {:<20}".format(bookNumber, member, loanStartReadable, loanEndReadable, loanLen, loanStatus))

    print(usersLate) 
    print(len(usersLate))
    print(len(users))
    print(totalDaysLate)
    return reportDict



books = openFile(booksFile)
loans = openFile(bookloansFile)
temp = buildTask3Details(loans)



