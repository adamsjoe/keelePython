import sys
import csv
import datetime
from pprint import pprint

#reportDict = {}

# csv file names
bookloansFile = 'bookloans.csv'
booksFile = 'books.csv'
reportFileTask3 = 'Task_3_report.csv'

LOAD_PERIOD = 14

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
    """Generate the content for the report.

    Keyword arguments:
    loans -- the list of data on the loans
    """
    reportDict = {}
    totalDaysLate = 0 # counter to count the number of total days late
    users = set() # used to store the UNIQUE members
    usersLate = set() #used to store the UNIQUE members who are late (bad members)
    totalLoansLate = 0    
    
    # print a nice header for the screen
    print ("{:<15} {:<10} {:<20} {:<20} {:<20}".format('book','member', 'start date', 'end date', 'days loaned'))
    
    # loop through all the rows in the loans (bookloans) file
    for row in loans:        
        
        # assign some commonly used columns to variables to make them more readable
        bookNumber = row[0]  
        #bookNumber = int(bookNumber)
        
        member = row[1] 
        loanStart = int(row[2]) # grab the loan start and make it an int
        loanEnd = int(row[3])  # grab the loan end and make it an int
        loanStartReadable = convertEpochToReadable(loanStart) # for the output, convert the loan start to a human readable format
        loanEndReadable = "" # loan end will be empty as it will depend if loan end is "0" or populated
        loanStatus = "" # again used for the report output
       
        daysLate = 0 # placeholder count for the number of days over 14 that any late items are
        loanLen = 0 # placeholder for loan length
        
        # if the loanEnd is not 0 (ie the item has been returned)
        if loanEnd != 0:
            # get the "human readable" version of the date
            loanEndReadable = convertEpochToReadable(loanEnd)
            # work out how long the loan was (we can simply subtract epoch dates for this)
            loanLen = loanEnd - loanStart
        else:
            # otherwise the item is still on loan
            loanEndReadable = "Item on loan"

        # be a smart ass and work out if the books on loan are overdue based on now date?
        if loanLen > LOAD_PERIOD:
            loanStatus = "Was Late"
            if member not in usersLate:
                usersLate.add(member)
            daysLate = loanLen - 14
            totalDaysLate += daysLate
            totalLoansLate += 1
        elif loanEnd != 0 and loanLen <=14:
            loanStatus = "Returned on time"        
        
        if member not in users:
            users.add(member)

        print("{:<15} {:<10} {:<20} {:<20} {:<20} {:<20}".format(bookNumber, member, loanStartReadable, loanEndReadable, loanLen, loanStatus))

    #print(usersLate) 
    print(">>",len(usersLate))
    print("<<",len(users))
    print(totalDaysLate)
    print(totalLoansLate)
    return reportDict



books = openFile(booksFile)
loans = openFile(bookloansFile)
temp = buildTask3Details(loans)



