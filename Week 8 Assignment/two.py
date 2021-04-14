import sys
import csv


class Library(object):

    def __init__(self, books_list):
        self.books_list = books_list

    def loan_book(self, book, member):
        pass

    def return_book(self, book):
        pass

    def reserve_book(self, book, member):
        pass


class LibraryMember(object):
    def __init__(self, id_no, first_name, last_name, gender, email, card_no):
        self._id_no = id_no
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._email = email
        self._card_no = card_no

    def list_members(self, members):
        print(
            "{:<12} {:<60} {:<40} {:<10}".format
            ('Member No.', 'First Name', 'Last Name', 'Card No.')
        )
        for obj in members:
            print(
                "{:<12} {:<60} {:<40} {:<10}".format
                (obj._id_no, 'Title', 'Author', 'Times Loaned 2019')
            )


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


def setup():
    # setup will need to do 1 of 2 things.
    # if we have no json file present, then we just load up
    # the csv files
    the_members = []
    the_books = [] 
    the_loans = []

    members = open_file('members.csv', True)
    books = open_file('books.csv', True)
    book_loans = open_file('bookloans.csv')

    for line in members:
        the_members.append(LibraryMember(
                                line[0],
                                line[1],
                                line[2],
                                line[3],
                                line[4],
                                line[5]
                                ))

    # the_books = []
    # for line in books:
    #     the_books.append(LibraryBook(
    #                             line[0],
    #                             line[2],
    #                             line[1],
    #                             line[3],
    #                             line[4],
    #                             line[5]
    #                             ))

    # the_loans = []
    # for line in book_loans:
    #     the_loans.append(BookLoan(
    #                             line[0],
    #                             line[1],
    #                             line[2],
    #                             line[3]
    #                             ))

def main_menu():
    done = False
    while done == False:
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
        if choice == "1":
            LibraryMember.list_members(the_members)
        elif choice == 2:
            issue_book_loan()
        elif choice == 3:
            book_returns()
        elif choice == 4:
            book_reservations()
        elif choice == "5":
            done = True
            sys.exit(0)
            break        
        #choice = int(choice)
        # need to handle non-ints
        #return int(choice)


# main thread of program
setup()
main_menu()
