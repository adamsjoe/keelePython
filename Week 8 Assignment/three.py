import csv
import json
import sys
import datetime
import os


# Constant filenames
BOOKLOANSFILE_CSV = 'bookloans.csv'
BOOKSFILE_CSV = 'books.csv'
MEMBERSFILE_CSV = 'members.csv'

BOOKLOANSFILE_JSON = 'bookloans.json'
BOOKSFILE_JSON = 'books.json'
MEMBERSFILE_JSON = 'members.json'
CURRENT_BOOKLOANSFILE_JSON = 'books_on_loan.json'
RESERVATIONSFILE_JSON = 'reservations.json'


# Constant headers
LOAN_HEADERS = ['Book_id', 'Member_id', 'Date_loaned', 'Date_returned']


# Class definition for a library book
class LibraryBook(object):
    """This object will be used to represent a library book.

    The constructor for this object takes in the values which
    are present in the CSV file for the books.  However to
    this 2 additional attributes are added.
    These additional attributes are:
    - if the book is available
    - If the book *is not* available the memeber who has it

    Methods
    -------
    printDetails(self)
        Prints the attributes for the current object

    scan(self)
        Returns the book number

    assign_to_user(self, member_id, book_data, member_data)
        Performs a "loan" operation for the given book to the given user

    return_item(self)
        Returns a book on loan and makes it available for another user

    """
    def __init__(self, book_number, author, title, genre, sub_genre,
                 publisher):
        self._book_number = book_number
        self._author = author
        self._title = title
        self._genre = genre
        self._sub_genre = sub_genre
        self._publisher = publisher
        self._available = check_book_loan_status(book_number,
                                                 currently_loaned_books)
        if self._available is True:
            self._loanee = None
        else:
            self._loanee = get_loaning_member(book_number,
                                              currently_loaned_books)
    """Prints out the data for the object passed in

    Arguments
    ---------
    self
    """
    def printDetails(self):
        print("Details for Book Number"), self._book_number
        print("--> Book Number      : ", self._book_number)
        print("--> Book Title       : ", self._title)
        print("--> Book Author      : ", self._author)
        print("--> Book Genre       : ", self._genre)
        print("--> Book Sub Genre   : ", self._sub_genre)
        print("--> Book Publisher   : ", self._publisher)
        print("--> Book Available?  : ", self._available)
        print("--> Loaned To Member : ", self._loanee)

    def scan(self):
        return self._book_number

    """Assigns a book to a user

    Arguments
    ---------
    memeber_id
        the user who will loan the book
    book_data
        the book object for the book to be loaned
    member_data
        the object for the member
    """
    def assign_to_user(self, member_id, book_data, member_data):
        self._available = False
        self._loanee = member_id

        # create a new dictionary
        data = {}
        data["Book_id"] = book_data.scan()
        data["Member_id"] = member_data.scan()
        data["Date_loaned"] = str(get_current_days_excel_epoch())
        data["Date_returned"] = "0"
        # update the books on loan json file
        update_books_on_loan(CURRENT_BOOKLOANSFILE_JSON, data)

        # update the bookloans.json file
        update_book_loans(BOOKLOANSFILE_JSON, data)

        # one of the design discussions raised the possibility
        # that a member could only borrow 5 items at a time,
        # this was not asked for, but it was something
        # easy to code for later
        member_data.increase_loan_items()

    def return_item(self):
        data = {}
        loans_info = open_json_file(BOOKLOANSFILE_JSON)
        for row in loans_info:
            if row["Book_id"] == self._book_number and \
               row["Date_returned"] == "0":
                print(row)
                data["Book_id"] = row["Book_id"]
                data["Member_id"] = row["Member_id"]
                data["Date_loaned"] = row["Date_loaned"]
                data["Date_returned"] = str(get_current_days_excel_epoch())

                # doing this at the end - not in place
                # print(data)
                update_json(BOOKLOANSFILE_JSON, data)
                # still need to do the user details decrease


class Member(object):

    max_id_number = 0

    def __init__(self, id_no, first_name, last_name, gender, email, card_no):
        if id_no is None:
            self._id_no = Member.max_id + 1
        else:
            self._id_no = int(id_no)
            Member.max_id = int(id_no)
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._email = email
        self._card_no = card_no
        if self._card_no != "0":
            self._card_issue_no = card_no[-1]
        else:
            self._card_issue_no = "None issued"
        self._no_of_loaned_items = get_loaned_items_cnt(id_no,
                                                        currently_loaned_books)

    def printDetails(self):
        print("--> Member ID number   : ", self._id_no)
        print("--> Member First Name  : ", self._first_name)
        print("--> Member Last Name   : ", self._last_name)
        print("--> Member Gender      : ", self._gender)
        print("--> Member Email       : ", self._email)
        print("--> Member Card No     : ", self._card_no)
        print("--> Member Card Issue  : ", self._card_issue_no)
        print("--> No of items loaned : ", self._no_of_loaned_items)
        # TODO Add in a count of reserved items?

    def assign_card_no(self, new_card_no):
        self._card_no = new_card_no

    def scan(self):
        return self._card_no

    def increase_loan_items(self):
        self._no_of_loaned_items += 1

    def decrease_loan_items(self):
        if self._no_of_loaned_items > 0:
            self._no_of_loaned_items -= 1
        else:
            print("Error: no returns on record")

    def apply(self):
        pass


class LibraryMember(Member):
    pass


def create_reservations_json(file_out, data=""):
    if os.path.isfile(file_out):
        print("{f} file exsists - no need to recreate\n".format(f=file_out))
    else:
        print(
            "{f} file does not exsist - recreating file..\n".format(f=file_out)
            )
        with open(file_out, 'w', encoding='utf-8') as json_file:
            jdata = []
            data = {}
            # data["Book_id"] = "1"
            # data["Member_id"] = "1"
            # data["Reserved_Date"] = "1"
            # jdata.append(data)
            jsonString = json.dumps(jdata, indent=4)
            json_file.write(jsonString)


def create_json(file_in, file_out, headers=False):

    if os.path.isfile(file_out):
        print("{f} file exsists - no need to recreate\n".format(f=file_out))
    else:
        print(
            "{f} file does not exsist - recreating file..".format(f=file_out)
            )
        # setup a variable to hold the data from the file
        data = []

        try:
            with open(file_in, encoding='utf-8-sig', mode='r') as file:
                if headers is False:
                    reader = csv.DictReader(file,)
                else:
                    reader = csv.DictReader(file, fieldnames=headers)
                for row in reader:
                    data.append(row)

            with open(file_out, 'w', encoding='utf-8') as json_file:
                jsonString = json.dumps(data, indent=4)
                json_file.write(jsonString)

        # handle file not found errors with a nice error message
        except FileNotFoundError:
            print('File {} does not exist.'.format(file_in))
            sys.exit(1)


# create a "books on loan" json file
def generate_books_on_loan_file(file_out, book_data, loans_data):

    if os.path.isfile(file_out):
        print(
            "{f} file exsists - no need to recreate\n".format(f=file_out)
            )
    else:
        print(
            "{f} file does not exsist - recreating file..".format(f=file_out)
            )
        jdata = []
        # parse through the books and then find out if the book is
        # loaned or now doing it this way eliminates books we don't
        # have in the books file (not asked for, but mention in writeup)
        for row in book_data:
            # parse the books and get the number
            book_id = row['Number']

            book_loaned = False
            # now parse the book loans to find the state
            for loan_row in loans_data:
                if loan_row['Book_id'] == book_id:
                    # print("Working on book id ", book_id)

                    if loan_row['Date_returned'] != '0':
                        # print("book is returned")
                        book_loaned = False
                    else:
                        # print('book is on loan')
                        book_loaned = True

                    if book_loaned is True:
                        data = {}
                        data["Book_id"] = loan_row["Book_id"]
                        data["Member_id"] = loan_row["Member_id"]
                        data["Date_loaned"] = loan_row["Date_loaned"]
                        data["Date_returned"] = loan_row["Date_returned"]
                        jdata.append(data)

        with open(file_out, 'w', encoding='utf-8') as filely:
            meh = json.dumps(jdata, indent=4)
            filely.write(meh)


def open_json_file(file):
    with open(file) as data:
        return_data = json.load(data)

    return return_data


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


def check_book_loan_status(book, loaned_books_list):
    if not any(d['Book_id'] == book for d in loaned_books_list):
        return True  # book is available
    else:
        return False  # book is already on loan


# could this be added to the library member class?
def get_loaned_items_cnt(member, loaned_books_list):
    count = 0
    for row in loaned_books_list:
        if member == row["Member_id"]:
            count += 1
    return count


# could this be added to the book class?
def get_loaning_member(book, loaned_books_list):
    for row in loaned_books_list:
        if book == row["Book_id"]:
            return row["Member_id"]


def validate_member(member_card, memberlist):
    for row in memberlist:
        data = None
        if member_card == row.scan():
            data = row  # member exists - return obj
            break
        else:
            data = False  # member is a lie
    return data


def validate_book(book, bookslist):
    data = None
    for row in bookslist:
        if book == row.scan():
            data = row  # book exists
            break
        else:
            data = False  # book is a lie
    return data


# make this pass in the file as a param
def update_books_on_loan(file_out, data):
    with open(file_out) as current_loans:
        currently_loaned_books = json.load(current_loans)

        currently_loaned_books.append(data)

    with open(file_out, "w") as file:
        json.dump(currently_loaned_books, file, indent=4)


def update_book_loans(file_out, data):
    with open(file_out) as current_loans:
        loans_data = json.load(current_loans)
        loans_data.append(data)

    with open(file_out, "w") as file:
        json.dump(loans_data, file, indent=4)


def update_members(file_out, data):
    with open(file_out) as members_now:
        mem_data = json.load(members_now)
        mem_data.append(data)

    with open(file_out, "w") as file:
        json.dump(mem_data, file, indent=4)


def update_json(file_out, data):
    with open(file_out) as file:
        file_data = json.load(file)
        file_data.append(data)

    with open(file_out, "w") as file:
        json.dump(file_data, file, indent=4)


# create json files from the CSV files
create_json(MEMBERSFILE_CSV, MEMBERSFILE_JSON)
create_json(BOOKSFILE_CSV, BOOKSFILE_JSON)
create_json(BOOKLOANSFILE_CSV, BOOKLOANSFILE_JSON, LOAN_HEADERS)
create_reservations_json(RESERVATIONSFILE_JSON)

# now open the JSON files
book_data = open_json_file(BOOKSFILE_JSON)
loans_data = open_json_file(BOOKLOANSFILE_JSON)
members_data = open_json_file(MEMBERSFILE_JSON)
reservvations_data = open_json_file(RESERVATIONSFILE_JSON)

# generate "books on loan" - an extra file
generate_books_on_loan_file(CURRENT_BOOKLOANSFILE_JSON, book_data, loans_data)

# this is never reloaded?
with open(CURRENT_BOOKLOANSFILE_JSON) as current_loans:
    currently_loaned_books = json.load(current_loans)

# now to create a list of objects of type LibraryBook
books = []
for line in book_data:
    books.append(LibraryBook(
                        line["Number"],
                        line["Author"],
                        line["Title"],
                        line["Genre"],
                        line["SubGenre"],
                        line["Publisher"]
                        ))

members = []
for line in members_data:
    members.append(LibraryMember(
                            line["ID"],
                            line["First Name"],
                            line["Last Name"],
                            line["Gender"],
                            line["Email"],
                            line["CardNumber"]
                            ))


#  TASK 1 CODE: loan a book
def loan_book():
    # get the membership card for the user
    # now validate this card is real
    while True:
        member_card = input("Please enter membership card number : ")
        mem_result = validate_member(member_card, members)
        if mem_result is not False:
            mem_result.printDetails()
            break
        else:
            print("{} is not recognised. Try again".format(member_card))
    print()

    # now validate the book is real
    while True:
        book_number = input("Please enter book number : ")
        book_result = validate_book(book_number, books)
        if book_result is not False:
            book_result.printDetails()
            break
        else:
            print("{} is not recognised. Try again".format(book_number))

    print()

    # check if book is able to be loaned
    if book_result._available is False:
        print("Cannot process - book already on loan")
        exit(0)
    else:
        print("Processing loan...")
        book_result.assign_to_user(mem_result._id_no, book_result, mem_result)
        book_result.printDetails()


# loan_book()

# TASK 2 CODE: return a book


def return_book():
    # to return a book, the librarian would just scan the barcode.
    while True:
        book_number = input("Please enter book number : ")
        book_result = validate_book(book_number, books)
        if book_result is not False:
            book_result.printDetails()
            break
        else:
            print("{} is not recognised. Try again".format(book_number))

    # check that this book is actually on loan
    if book_result._available is True:
        # we cannot return what is not issued
        print("'{}' is not issued.".format(book_result._title))
        print("Unable to process a return.")
        exit(0)
    else:
        book_result.return_item()
        # find the element in the JSON file


# return_book()
# TASK 3 CODE: apply for membership
def do_apply():
    new_f_name = input("Please enter first name    : ")
    new_l_name = input("Please enter last name     : ")
    new_gender = input("Please enter gender        : ")
    new_email = input("Please enter email address : ")

    # we need to check that this person does not exist
    for row in members:
        if row._first_name.lower() == new_f_name.lower() and \
            row._last_name.lower() == new_l_name.lower() and \
            row._gender.lower() == new_gender.lower() and \
                row._email == new_email:
            print("Member already exists.  Cannot apply again.")
            sys.exit(0)

    # then we need to add him to the users list
    # ensure that the text is all nice and uniform
    new_f_name = new_f_name.title()
    new_l_name = new_l_name.title()
    new_gender = new_gender.title()
    new_email = new_email.lower()

    # create a new LibraryMember objct
    members.append(LibraryMember(
                            None,
                            new_f_name,
                            new_l_name,
                            new_gender,
                            new_email,
                            "0"
                            ))

    data = {}
    for row in members:
        if row._first_name.lower() == new_f_name.lower() and \
            row._last_name.lower() == new_l_name.lower() and \
            row._gender.lower() == new_gender.lower() and \
                row._email == new_email:
            data["ID"] = str(row._id_no)
            data["First Name"] = row._first_name
            data["Last Name"] = row._last_name
            data["Gender"] = row._gender
            data["Email"] = row._email
            data["CardNumber"] = "0"

    update_members(MEMBERSFILE_JSON, data)


# do_apply()

# TASK 4 CODE: reserve a book

# to reserve a book, we will need to check if the book is on loan.

def do_reserve():
    data = {}
    while True:
        book_number = input("Please enter book number : ")
        book_result = validate_book(book_number, books)
        if book_result is not False:
            book_result.printDetails()
            break
        else:
            print("{} is not recognised. Try again".format(book_number))

    # check if book is able to be loaned
    if book_result._available is True:
        print("Cannot process - '{}' is not loaned".format(book_result._title))
        sys.exit(0)
    else:
        print("We can do this")

    while True:
        member_card = input("Please enter membership card number : ")
        mem_result = validate_member(member_card, members)
        if mem_result is not False:
            mem_result.printDetails()
            break
        else:
            print("{} is not recognised. Try again".format(member_card))

    data["Book_id"] = str(book_result._book_number)
    data["Member_id"] = str(mem_result._id_no)
    data["Reserved_Date"] = str(get_current_days_excel_epoch())

    # print(data)
    # not working
    update_json(RESERVATIONSFILE_JSON, data)


do_reserve()
# TASK 5 CODE: notification system
