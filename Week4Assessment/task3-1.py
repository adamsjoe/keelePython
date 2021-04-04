import sys
import csv
import datetime

# csv file names
BOOKLOANSFILE = 'bookloans.csv'
BOOKSFILE = 'books.csv'
REPORTFILETASK3 = 'Task_3_report.csv'

LOAN_PERIOD = 14


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


def get_current_days_excel_epoch():
    """Calculates the number of days since 1-1-1900 (the Excel Epoch)

    Keyword arguements: 
        none

    Returns:
        delta.days = a integer value representing number of days since
        1-1-1900
    """
    f_date = datetime.date(1900, 1, 1)
    l_date = datetime.datetime.today().date()

    delta = l_date - f_date
    return delta.days


def sort_and_generate_task3_content(data_in):
    """Sorts  the dictionary which is passed in
    on the field timesOutIn2019 and then converts
    this to a list for use with the CSV writer function.

    This function also prints to the screen the report to provide
    the user with some indication that the task in underway.

    Keyword arguments:
        dataIn --  the dictionary which was built up in the
        sort_and_generate_task3_content function.

    Returns:
        report_out -- a listed sorted on timesOutIn2019

    """
    report_out = []
    print(
        "{:<20} {:<30} {:<30} {:<30}".format
        ('Member Number', 'Average Loan Length (Days)',
         'Average Late Period (Days)', 'Instances Late')
        )

    for k, v in sorted(data_in.items(), key=lambda e: e[1]["noOfLateTimes"], reverse=True):
        if v['totalLateDays'] == 0 or v['noOfLateTimes'] == 0:
            average_late = 0
            average_loan = 0
        else:

            average_late = v['totalLateDays'] / v['noOfLateTimes']
            average_loan = v['loanedDays'] / v['noOfNotLateTimes']

            average_late = round(average_late, 2)
            average_loan = round(average_loan, 2)

        item = [k, average_loan, average_late, v['noOfLateTimes']]
        report_out.append(item)
        print(
            "{:<20} {:<30} {:<30} {:<30}".format
            (k, average_loan, average_late, v['noOfLateTimes'])
        )
    return report_out


def get_percentages_data(data_in):
    """Calculates the percentage of users who have returned an item late.
    Also returns:
    - Number of users
    - Number of users who have never returned anything late
    - Number of users who have returned an item late

    Keyword Arguements:
        data_in -- list from the sort function
    
    Returns:
        small list with the 4 items in the descrption returned.
    """

    data_out = []
    good_users = 0
    no_of_users = len(data_in)

    for item in data_in:
        if item[3] == 0:
            # this user has never been late
            good_users += 1

    no_of_late_users = no_of_users - good_users
    percentage_late_users = (no_of_late_users / no_of_users) * 100

    item = [no_of_users, good_users, no_of_late_users, percentage_late_users]
    data_out.append(item)
 
    print(
        "{:<20} {:<30} {:<30} {:<30}".format
        ('Total Users',
         'Users never been late',
         'Users with late returns',
         'Percentage users been late')
    )
    print(
        "{:<20} {:<30} {:<30} {:<30}".format
        (no_of_users, good_users, no_of_late_users, str(percentage_late_users) + "%")
    )

    return data_out


def build_task3_details(loans):
    """Generate the content for the report.

    This function will parse the loans file and return a dictionary
    of dictionaries which contains the data on:
    - total number of days a member loaned books
    - total instances of non late returns
    - total instances of late returns
    - total number of days late

    Keyword arguments:
        loans -- the list of data on the loans

    Returns:
        report_dict -- a dictionary (keyed on member)
        containing info above
    """
    report_dict = {}
    for row in loans:
        book_late = False
        noOfLateDays = 0

        # get the member number
        member_number = row[1]
        member_number = int(member_number)

        # get the date loaned
        date_loaned = row[2]
        date_loaned = int(date_loaned)

        # get the date returned
        date_returned = row[3]
        date_returned = int(date_returned)

        # if date returned == 0 then the book is on loan,
        # we should determine if that means it is currently
        # late or not
        if date_returned == 0:
            date_returned = get_current_days_excel_epoch()

        # loan_length will be the difference between the
        # end of the loan and the start of the loan
        loan_length = date_returned - date_loaned

        # if date returned is greater than than start of
        # loan + 14 (LOAN PERIOD)
        # then the book is late.
        if date_returned > (date_loaned + LOAN_PERIOD):
            # then the book was late
            book_late = True
            # and work out late by how many days
            noOfLateDays = loan_length - LOAN_PERIOD

        # to start recording the info
        # first check if the member number exists
        # this creates the structure for each member
        if member_number not in report_dict:
            report_dict[member_number] = {}
            report_dict[member_number]["noOfLateTimes"] = 0
            report_dict[member_number]["noOfNotLateTimes"] = 0
            report_dict[member_number]["totalLateDays"] = 0
            report_dict[member_number]["loanedDays"] = 0

        if member_number in report_dict:
            # retrieve the info for the member
            lateTimesDict = report_dict[member_number].get("noOfLateTimes")
            nonLateTimesDict = report_dict[member_number].get("noOfNotLateTimes")
            sumOfAllLateDaysDict = report_dict[member_number].get("totalLateDays")
            sumLoanLenDict = report_dict[member_number].get("loanedDays")

            # if book was late, increment the late counter, or the non-late
            if book_late is True:
                lateTimesDict += 1
                sumOfAllLateDaysDict += noOfLateDays
            else:
                nonLateTimesDict += 1

            sumLoanLenDict += loan_length

            # now write this back to our dictionary
            report_dict[member_number]["noOfLateTimes"] = lateTimesDict
            report_dict[member_number]["noOfNotLateTimes"] = nonLateTimesDict
            report_dict[member_number]["totalLateDays"] = sumOfAllLateDaysDict
            report_dict[member_number]["loanedDays"] = sumLoanLenDict

    return report_dict


late_user_report_headers = ['Member Number',
                            'Average Loan Length',
                            'Average Late Period'
                            ]
percentage_headers = ['Total Number of Users',
                      'Users who have never been late',
                      'Number of users with late returns',
                      'Percentage of users with late returns'
                      ]

loans = open_file(BOOKLOANSFILE)
temp = build_task3_details(loans)
users_data = sort_and_generate_task3_content(temp)

percentage_data = get_percentages_data(users_data)

create_report(REPORTFILETASK3, late_user_report_headers, users_data)
create_report(REPORTFILETASK3, percentage_headers, percentage_data)
