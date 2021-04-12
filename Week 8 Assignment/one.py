import sys
import csv
from os import system, name


class LibraryMember(object):
    def __init__(self, id_no, first_name, last_name, gender, email, card_no):
        self._id_no = id_no
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._email = email
        self._card_no = card_no

    def printDetails(self):
        print("Member ID number: ", self._id_no)
        print("--> Member First Name: ", self._first_name)
        print("--> Member Last Name : ", self._last_name)
        print("--> Member Gender    : ", self._gender)
        print("--> Member Email     : ", self._email)
        print("--> Member Card No.  : ", self._card_no)

    def assign_card_no(self, new_card_no):
        self._card_no = new_card_no

    def scan(self):
        return self._id_no


class LibraryBook(object):
    def __init__(self, book_number, author, title, genre, sub_genre,
                 publisher):
        self._book_number = book_number
        self._author = author
        self._title = title
        self._genre = genre
        self._sub_genre = sub_genre
        self._publisher = publisher

    def scan(self):
        return self._book_number


class BookLoan(object):
    def __init__(self, book_number, member_number, date_out, date_returned):
        self._book_number = book_number
        self._member_number = member_number
        self._date_out = date_out
        self._date_returned = date_returned


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


def main_menu():
    strs = ('Enter 1 for Member Services\n'
            'Enter 2 for Book Loans\n'
            'Enter 3 for Book Returns\n'
            'Enter 4 for Book Reservations\n'
            'Enter 5 to exit : ')
    choice = input(strs)
    return int(choice)


def issue_book_loan():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                        BOOK LOAN                               *")
    print("*                                                                *")
    print("******************************************************************")
    print()
    print()
    print()
    # need to check here and do a search that the book and member both exist
    member = input("Please enter a member card number: ")
 
    for obj in the_members:
        if obj._id_no == member:
            print("member found")
            obj.printDetails()

    book_id_no = input("Please enter a book number: ")
    return True


def book_returns():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                       BOOK RETURN                              *")
    print("*                                                                *")
    print("******************************************************************")
    return True


def member_services():
    clear()
    print("******************************************************************")
    print("*                                                                *")
    print("*                     MEMBER SERVICES                            *")
    print("*                                                                *")
    print("******************************************************************")
    return True


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


members = open_file('members.csv', True)
books = open_file('books.csv', True)
book_loans = open_file('bookloans.csv')


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
