import csv
import json
import sys

BOOKLOANSFILE_CSV = 'bookloans.csv'
BOOKSFILE_CSV = 'books.csv'
MEMBERSFILE_CSV = 'members.csv'

BOOKLOANSFILE_JSON = 'bookloans.json'
BOOKSFILE_JSON = 'books.json'
MEMBERSFILE_JSON = 'members.json'
CURRENT_BOOKLOANSFILE_JSON = 'books_on_loan.json'

LOAN_HEADERS = ['Book_id', 'Member_id', 'Date_loaned', 'Date_returned']


def create_json(file_in, file_out, headers=False):
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
            # jsonString = json.dump(data, json_file)
            json_file.write(jsonString)

    # handle file not found errors with a nice error message
    except FileNotFoundError:
        print('File {} does not exist.'.format(file_in))
        sys.exit(1)


# create json files from the CSV files
create_json(MEMBERSFILE_CSV, MEMBERSFILE_JSON)
create_json(BOOKSFILE_CSV, BOOKSFILE_JSON)
create_json(BOOKLOANSFILE_CSV, BOOKLOANSFILE_JSON, LOAN_HEADERS)

# create a "library" :
# this will, for each book, determing if it's "loaned" or not
# first let#s get the json files
with open('books.json') as booksfile:
    book_data = json.load(booksfile)

with open('bookloans.json') as bookloansfile:
    loans_data = json.load(bookloansfile)

with open('members.json') as membersfile:
    members_data = json.load(membersfile)

# some placeholders
jdata = []
# parse through the books and then find out if the book is loaned or now
# doing it this way eliminates books we don't have in the books file (not asked
# for, but mention in writeup)
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


with open(CURRENT_BOOKLOANSFILE_JSON, 'w', encoding='utf-8') as filely:
    meh = json.dumps(jdata, indent=4)
    filely.write(meh)

with open(CURRENT_BOOKLOANSFILE_JSON) as current_loans:
    currently_loaned_books = json.load(current_loans)


def check_book_loan_status(book, loaned_books_list):
    if not any(d['Book_id'] == book for d in loaned_books_list):
        return True  # book is available
    else:
        return False  # book is already on loan


def get_loaned_items_cnt(member, loaned_books_list):
    count = 0
    for row in loaned_books_list:
        if member == row["Member_id"]:
            count += 1
    return count


def get_loaning_member(book, loaned_books_list):
    # print(book)
    # print("--")
    for row in loaned_books_list:
        if book == row["Book_id"]:
            return row["Member_id"]


def validate_member(member_card, memberlist):
    for row in memberlist:
        if member_card == row.scan():
            return row  # member exists - return obj
        else:
            return False  # member is a lie


def validate_book(book, bookslist):
    for row in bookslist:
        if book == row.scan():
            return row  # book exists
        else:
            return False  # book is a lie


def do_return(book):
    pass


def do_reserve_book(book, member):
    # will need to check the book is not available before proceeding
    pass


def do_apply():
    pass


def do_startup_check():
    # if the json files are present then no need to regenerate them
    # just load the data
    pass


# Class definition for a library book
class LibraryBook(object):
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

    def assign_to_user(self, member_id):
        self._available = False
        self._loanee = member_id


# now to create a list of objects of type LibraryBook
books = []
for line in book_data:
    books.append(LibraryBook(
                        line["Number"],
                        line["Title"],
                        line["Author"],
                        line["Genre"],
                        line["SubGenre"],
                        line["Publisher"]
                        ))


class LibraryMember(object):

    max_id = 0

    def __init__(self, id_no, first_name, last_name, gender, email, card_no):
        self._id_no = id_no
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

    def assign_card_no(self, new_card_no):
        self._card_no = new_card_no

    def scan(self):
        return self._card_no


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


# # we now have a list of objects for the books.  Each book has a
# # state (available to loan)
# for row in books:
#     print(row.printDetails())

# for row in members:
#     print(row.printDetails())


def append_to_json(file, data):
    with open(file, 'w', encoding='utf-8') as json_file:
        jsonString = json.dumps(data, indent=4)
        # jsonString = json.dump(data, json_file)
        json_file.write(jsonString)


def do_loan():
    member = input("enter member card number : ")
    real_member = validate_member(member, members)

    book_to_take = input("enter book number : ")
    real_book = validate_book(book_to_take, books)

    # print book stats
    real_book.printDetails()

    real_book.assign_to_user(real_member.scan())

    real_book.printDetails()

    # works but uses global stuff
    data = {}
    data["Book_id"] = real_book.scan()
    data["Member_id"] = real_member.scan()
    data["Date_loaned"] = "today"
    data["Date_returned"] = "0"
    jdata.append(data)

    # then save this
    append_to_json(CURRENT_BOOKLOANSFILE_JSON, jdata)


# do_loan()
# print(currently_loaned_books)
