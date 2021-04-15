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

loan_headers = ['Book_id', 'Member_id', 'Date_loaned', 'Date_returned']
create_json(BOOKLOANSFILE_CSV, BOOKLOANSFILE_JSON, loan_headers)

# create a "library" :
# this will, for each book, determing if it's "loaned" or not
# first let#s get the json files
# TODO add a check, if not present, generate from the csv
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


# check if the book is on loan (ie if it is present in the currently on
# loan list, it is on loan)
# if not any(d['Book_id'] == '1' for d in currently_loaned_books):
#     print("book not on loan")

# book_to_check = input("Enter book Number : ")

# state = check_book_loan_status(book_to_check, currently_loaned_books)

# print("The book is available : ", state)


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

    def printDetails(self):
        print("Details for Book Number"), self._book_number
        print("--> Book Number      : ", self._book_number)
        print("--> Book Title       : ", self._title)
        print("--> Book Author      : ", self._author)
        print("--> Book Genre       : ", self._genre)
        print("--> Book Sub Genre   : ", self._sub_genre)
        print("--> Book Publisher   : ", self._publisher)
        print("--> Book Available?  : ", self._available)

    def scan(self):
        return self._book_number


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
# we now have a list of objects for the books.  Each book has a
# state (available to loan)
for row in books:
    print(row.printDetails())
    

def do_loan(lendee, book):
    pass

def validate_member(member):
    pass

def validate_book(book):
    pass

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