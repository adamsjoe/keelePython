import sys
import csv
import datetime

# csv file names
BOOKLOANSFILE = 'bookloans.csv'
BOOKSFILE = 'books.csv'
REPORTFILETASK_1 = 'Task_1_report.csv'


def open_file(file_in, skip_header=False):
    """Open a file and returns the data.

        Wraps a basic file open in a function to allow this
        to be reused.  When I was examining the books and
        bookloans files I noticed that when reading the
        files, I always ended up with a very random
        "\ufeff1" appearing right at the begning of the data
        from the file.  Further examination with VS Code
        showed that the encoding of the file was "utf-8 with
        BOM" and that this random sequence was a symptom.
        To corrrect this, the file had to be opened with
        "utf-8-sig" encoding.  I did consider if the
        encoding should also be made a parameter, but
        ultimately for these tasks kept this hard coded
        as both files share the same encoding.

        I also try to catch errors using a try/except
        block, I have one specific error "FileNotFoundError"
        and a generic catch all.  Error messages for both
        these occasions make use of string formatting to pass
        the fileIn parameter, which futher enhances re-usability.
        I fruther call sys.exit(1) which stops the execution
        and allows the OS to know there was a problem.

        I have checked the FileNotFound exception by passing
        in the name of a non-existing file.

        Keyword arguments:
            fileIn -- the file object whi chwill be opened
            skipHeader -- some files have "Headers" in the
            first row, if this is true we ignore these
            (defaults to False) Ultimatley, I never used
            this parameter

        Returns:
            data -- a list of tuples
    """
    # setup a variable to hold the data from the file
    data = ''
    try:
        with open(file_in, encoding='utf-8-sig', mode='r') as file:
            reader = csv.reader(file)
            if skip_header is True:
                # if skip_header is true, then skip to the next line
                next(reader, None)
            # make each row in the input file into a tuple and add
            # this to a list to be returned.
            data = [tuple(row) for row in reader]
    # handle file not found errors with a nice error message
    except FileNotFoundError:
        print('File {} does not exist.'.format(file_in))
        sys.exit(1)
    except:  # generic catch all error message
        print(
            'Trying to open {} failed.  No further information was available'
            .format(file_in))
        sys.exit(1)
    # return the data variable (the file contents)
    return data


def convert_epoch_to_readable(date_in):
    """Convert Excel Epoch time to a sting.

    This strange epoch format was a challenge for me.  In order to check if
    the date was in 2019 (which was asked for in the question) the only
    way I could think was to convert this format to something "human"
    readable and then check for the year.  This function simply takes
    in the epoch date and passes out a human readable string.

    Note:
    Excel has a strange idea of epoch, as well a bug from Lotus notes,
    to convert the date to a readable format I used the following code,
    which was taken from the  Stackover Flow post referenced:

    Before using this function, I tested this by taking the date
    columns in the bookloans.csv and converting them to "date"
    format.
    I then checked that the dates returned by the function matched
    those of excel.  They did.

        Keyword arguments:
            dateIn -- the date (in excel epoch) format

        Returns:
            dateOut -- a date in string format (eg 12-01-1996)
    """
    # Mac and PC excel have different "start dates" - using a PC, but
    # leaving the mac code in if needed.
    EXCEL_DATE_SYSTEM_PC = 1900

    dateOut = datetime.date(EXCEL_DATE_SYSTEM_PC, 1, 1) + datetime.timedelta(date_in-2)

    dateOut = dateOut.strftime("%d-%m-%Y")

    return dateOut


def contains_date(stringDate, dateToCheck):
    """Checks if a string contains another String.

    This takes two strings and returns a boolean if there is a substring match.
    This is marked as "containsDate" but it is essentially a substring matching
    function and could be renamed and still not loose any readability or
    functionality.

        Keyword arguments:
            stringDate -- a date in string format, in truth this could be ANY
            string.
            dateToCheck -- a part of the date to check, in truth this could be
            any string.
    """
    # basic substring matching here.  If we find the substring, return True,
    # else return False.
    if dateToCheck in stringDate:
        return True
    else:
        return False


def build_task1_details(loans):
    """Generate the content for the report.

    Keyword arguments:
        loans -- the list of data from the loans CSV file

    Returns:
        report_dict -- a dictionary (keyed on booknumber) containing
        times loaned in 2019, the title, the author
    """
    report_dict = {}
    for row in loans:
        # make things easier to reference
        book_number = row[0]
        book_number = int(book_number)

        # get the loaned date, convert this to an int and convert
        # to a readable string
        loaned_date_epoch = row[2]
        loaned_date_epoch = int(loaned_date_epoch)
        loaned_date_readable = convert_epoch_to_readable(loaned_date_epoch)

        # We will store the info on the books in a nested dictionary using the
        # book number as a key.
        # First ensure the book_number is not already present:
        if book_number not in report_dict:
            report_dict[book_number] = {}

        if book_number in report_dict:
            # we need to check if the book which is being loaned is present in
            # our cut down books.csv
            book_found = False

            # loop through the books
            for book in books:
                book_ref = book[0]
                # bit sucky, to keep code working I had to bring in the
                # headers. This makes sure we don't deal with the headers
                if book_ref != 'Number':
                    book_ref = int(book_ref)
                if book_ref == book_number:
                    book_found = True
            if book_found:
                # we have found the book - so add the author and title to
                # fields.
                book_title = books[book_number][1]
                book_author = books[book_number][2]
                if contains_date(loaned_date_readable, '2019'):
                    # if the book was loanded in 2019, get the number of
                    # times this has been out.
                    loaned_times = report_dict[book_number].get("timesOut2019")

                    # However, we may get a None type.  In this occasion,
                    # we can assume the bookNumber isn't in the dictionary,
                    # so set the loanedTimes as 1
                    if loaned_times is None:
                        loaned_times = 1
                    else:
                        loaned_times += 1
            else:
                # if the book wasn't found, then we blank out the name
                # and author
                book_title = ""
                book_author = ""

        else:
            # this is a new book
            report_dict[book_number]["timesOut2019"] = 1

        # add to fields only if the bookTitle is not an empty string
        if book_title != "":
            # we write this to reportDict
            report_dict[book_number]["timesOut2019"] = loaned_times
            report_dict[book_number]["title"] = book_title
            report_dict[book_number]["author"] = book_author
        else:
            # if the bookTitle is empty, then we also need to remove the
            # booknumber from the final report
            report_dict.pop(book_number)

    return report_dict


def sort_and_generate_task1_content(data_in):
    """Sorts  the dictionary which is passed in
    on the field timesOutIn2019 and then converts
    this to a list for use with the CSV writer function.

    This function also prints to the screen the report to provide
    the user with some indication that the task in underway.

    Keyword arguments:
        dataIn --  the dictionary which was built up in the
        buildTask1Details function.

    Returns:
        report_out -- a listed sorted on timesOutIn2019

    """
    report_out = []
    print(
        "{:<12} {:<60} {:<40} {:<10}".format
        ('Book Number', 'Title', 'Author', 'Times Loaned 2019')
        )
    for k, v in sorted(data_in.items(), key=lambda e: e[1]["timesOut2019"]):
        item = [k, v['title'], v['author'], v['timesOut2019']]
        report_out.append(item)
        print(
            "{:<12} {:<60} {:<40} {:<10}".format
            (k, v['title'], v['author'], v['timesOut2019'])
        )
    return report_out


def create_report(file_name, headers, content):
    """Creates a report file (currently a CSV)

    Keyword arguments:
        file_name -- the file we wish to create
        headers -- a list containing the header columns for the report
        content -- a list with the data to be populated in the file.
    """
    try:
        with open(file_name, 'a', newline="") as out_file:
            csvwriter = csv.writer(out_file)
            csvwriter.writerow(headers)
            csvwriter.writerows(content)
    except:
        print(
            'Trying to create {} failed.  No further information was available'
            .format(file_name)
        )
        sys.exit(1)


# Task 1 specific code

# The headers for our report
report_headers = ['Book Number', 'Title', 'Author', 'Times Loaned 2019']

# Open the CSV files and assign them to variables
books = open_file(BOOKSFILE)
loans = open_file(BOOKLOANSFILE)

temp = build_task1_details(loans)
contents = sort_and_generate_task1_content(temp)
create_report(REPORTFILETASK_1, report_headers, contents)
