import csv
import json
import sys
import datetime
import os
from pprint import pprint


# Constant filenames
BOOKLOANSFILE_CSV = 'bookloans.csv'
BOOKSFILE_CSV = 'books.csv'
MEMBERSFILE_CSV = 'members.csv'

BOOKLOANSFILE_JSON = 'bookloans.json'
BOOKSFILE_JSON = 'books.json'
MEMBERSFILE_JSON = 'members.json'
CURRENT_BOOKLOANSFILE_JSON = 'books_on_loan.json'

# Constant headers
LOAN_HEADERS = ['Book_id', 'Member_id', 'Date_loaned', 'Date_returned']


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

    def loan_book(self, member):
        pass


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

    def assign_card_no(self, new_card_no):
        self._card_no = new_card_no

    def scan(self):
        return self._card_no


class LibraryMember(Member):
    pass


def create_json(file_in, file_out, headers=False):

    if os.path.isfile(file_out):
        print("{f} file exsists - no need to recreate\n".format(f=file_out))
    else:
        print("{f} file does not exsist - recreating file..".format(f=file_out))
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


def open_json_file(file):
    with open(file) as data:
        return_data = json.load(data)

    return return_data


def replace_json_file(file, data):
    with open(file, 'w', encoding='utf-8') as json_file:
        jsonString = json.dumps(data, indent=4)
        # jsonString = json.dump(data, json_file)
        json_file.write(jsonString)


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


# create json files from the CSV files
create_json(MEMBERSFILE_CSV, MEMBERSFILE_JSON)
create_json(BOOKSFILE_CSV, BOOKSFILE_JSON)
create_json(BOOKLOANSFILE_CSV, BOOKLOANSFILE_JSON, LOAN_HEADERS)

book_data = open_json_file(BOOKSFILE_JSON)
loans_data = open_json_file(BOOKLOANSFILE_JSON)
members_data = open_json_file(MEMBERSFILE_JSON)

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


# for row in members:
#    print(row.printDetails())

#pprint(members_data)

#  TASK 1 CODE:

def loan_book():
    # get the membership card for the user
    

    # now validate this card is real
    while True:
        member_card = input("Please enter membership card number : ")
        mem_result = validate_member(member_card, members)
        if mem_result is not False:
            mem_result.printDetails()
            break
    print()
    while True:
        book_number = input("Please enter book number : ")
        book_result = validate_book(book_number, books)
        if book_result is not False:
            book_result.printDetails()
            break


loan_book()