import sys
import csv
from os import system, name
import time


# Class definitions
class LibraryMember(object):
    def __init__(self, id_no, first_name, last_name, gender, email, card_no):
        self._id_no = id_no
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._email = email
        self._card_no = card_no

    def printDetails(self):
        print("Details for Card Number"), self._card_no
        print("--> Member ID number  : ", self._id_no)
        print("--> Member First Name : ", self._first_name)
        print("--> Member Last Name  : ", self._last_name)
        print("--> Member Gender     : ", self._gender)
        print("--> Member Email      : ", self._email)

    def assign_card_no(self, new_card_no):
        self._card_no = new_card_no

    def scan(self):
        return self._card_no


class LibraryBook(object):
    def __init__(self, book_number, author, title, genre, sub_genre,
                 publisher):
        self._book_number = book_number
        self._author = author
        self._title = title
        self._genre = genre
        self._sub_genre = sub_genre
        self._publisher = publisher

    def printDetails(self):
        print("Details for Book Number"), self._book_number
        print("--> Book Title       : ", self._title)
        print("--> Book Author      : ", self._author)
        print("--> Book Genre       : ", self._genre)
        print("--> Book Sub Genre   : ", self._sub_genre)
        print("--> Book Publisher   : ", self._publisher)

    def scan(self):
        return self._book_number


class BookLoan(object):
    def __init__(self, book_number, member_number, date_out, date_returned):
        self._book_number = book_number
        self._member_number = member_number
        self._date_out = date_out
        self._date_returned = date_returned


# function definitions
def open_file(file_in, skip_header=False):
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
    # return the data variable (the file contents)
    return data


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def get_members_awaiting_cards():
    # total_members = len(the_members)
    awaiting_card = 0

    for obj in the_members:
        if obj._card_no == 0:
            awaiting_card += 1

    return awaiting_card


def main_menu():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                      LIBRARY SYSTEM                            *")
    print("*                                                                *")
    print("******************************************************************")
    strs = ('Enter 1 for Member Services\n'
            'Enter 2 for Book Loans\n'
            'Enter 3 for Book Returns\n'
            'Enter 4 for Book Reservations\n'
            'Enter 5 to exit : ')
    choice = input(strs)
    # need to handle non-ints
    return int(choice)


def issue_book_loan():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                        BOOK LOAN                               *")
    print("*                                                                *")
    print("******************************************************************")
    return True


def book_returns():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                       BOOK RETURN                              *")
    print("*                                                                *")
    print("******************************************************************")
    return True


def member_details():
    # clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                      MEMBER DETAILS                            *")
    print("*                                                                *")
    print("******************************************************************")
    print()
    print()
    member = input("Please enter member id number: ")

    for obj in the_members:
        if obj._id_no == member:

            card_num = ""
            issue_num = ""

            if obj._card_no == "0":
                card_num = "No card issued"
                issue_num = "No card issued"
            else:
                card_len = len(obj._card_no)
                issue_num = obj._card_no[-1]  # this is flaw - can only have 9 cards issues
                card_num = obj._card_no[0: card_len - 1]

            print("******************************************************************")
            print("* First Name   : ", obj._first_name.upper())
            print("* Last Name    : ", obj._last_name.upper())
            print("* Gender       : ", obj._gender.upper())
            print("* E-mail       : ", obj._email)
            print("* Card Number  : ", card_num.upper())
            print("* Card Issue   : ", issue_num.upper())
            print("******************************************************************")
            print()
            choice2 = input("Return to member services (Y/N)")
            choice2 = choice2.upper()  # shit
            while choice2 != 'Y':
                choice2 = choice2.upper()
                choice2 = input("Return to member services (Y/N)")
            return True


def member_services():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                     MEMBER SERVICES                            *")
    print("*                                                                *")
    print("******************************************************************")
    print()
    print()
    count = get_members_awaiting_cards()
    print("Number of members awaiting cards: ", count, "\n")
    strs = ('Enter 1 for Member Details\n'
            'Enter 2 for Member Application\n'
            'Enter 3 to return to main menu : ')

    choice = input(strs)
    if int(choice) == 1:
        member_details()
    elif int(choice) == 2:
        member_application()
    elif int(choice) == 3:
        return True


def validate_email_address_format(email_in):
    if '@' in email_in:
        return True
    else:
        return False


def create_member(f_name, l_name, gender,e_mail):
    # get the largest id
    # call a write function
    pass


def member_application():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                    MEMBER APPLICATION                          *")
    print("*                                                                *")
    print("******************************************************************")
    print()
    print()
    new_member_first_name = input("Enter first name : ")
    new_member_last_name = input("Enter last name : ")
    new_member_gender = input("Enter gender : ")
    valid_email = False
    while valid_email is not True:
        new_member_email = input("Enter email address : ")
        valid_email = validate_email_address_format(new_member_email)

    # now check the user does not already exist - make this a function
    for obj in the_members:
        if obj._first_name.lower() == new_member_first_name.lower() and obj._last_name.lower() == new_member_last_name.lower() and obj._gender.lower() == new_member_gender.lower() and obj._email.lower() == new_member_email.lower():
            print("USER ALREADY EXISTS")
            time.sleep(5)
        else:
            create_member(new_member_first_name, new_member_last_name, new_member_gender, new_member_email)
            # create user in the file

    


def book_reservations():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                    BOOK RESERVATION                            *")
    print("*                                                                *")
    print("******************************************************************")
    return True


def good_bye():
    clear()
    print("Thank you and have a nice day.")
    # TODO cleanup here - like save files
    sys.exit(0)


def send_email(addressee, subject, body):
    print("Sending email to '{}' with the subject '{}' and body '{}"
          .format(addressee, subject, body))


# main thread
members = open_file('members.csv', True)
books = open_file('books.csv', True)
book_loans = open_file('bookloans.csv')


# create a list of objects for library members
the_members = []
for line in members:
    the_members.append(LibraryMember(
                            line[0],
                            line[1],
                            line[2],
                            line[3],
                            line[4],
                            line[5]
                            ))

# create a list of objects for books
the_books = []
for line in books:
    the_books.append(LibraryBook(
                            line[0],
                            line[2],
                            line[1],
                            line[3],
                            line[4],
                            line[5]
                            ))

the_loans = []
for line in book_loans:
    the_loans.append(BookLoan(
                            line[0],
                            line[1],
                            line[2],
                            line[3]
                            ))


# notes to ask
# can we only use json, time, csv imports?
# do we need to care about numbers of books? (ie book loans, do we need to
# check if we have "stock" of a book?)
while True:
    choice = main_menu()
    if choice == 1:
        member_services()
    elif choice == 2:
        issue_book_loan()
    elif choice == 3:
        book_returns()
    elif choice == 4:
        book_reservations()
    elif choice == 5:
        good_bye()
        break
