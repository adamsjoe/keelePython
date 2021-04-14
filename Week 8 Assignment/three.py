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


with open('books.json') as booksfile:
    book_data = json.load(booksfile)

with open('bookloans.json') as bookloansfile:
    loans_data = json.load(bookloansfile)

with open('members.json') as membersfile:
    members_data = json.load(membersfile)

data = {}
jdata = []
# doing it this way eliminates books we don't have in the books file
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
                data["Book_id"] = loan_row["Book_id"]
                data["Member_id"] = loan_row["Member_id"]
                data["Date_loaned"] = loan_row["Date_loaned"]
                data["Date_returned"] = loan_row["Date_returned"]
                jdata.append(data)

with open(CURRENT_BOOKLOANSFILE_JSON, 'w', encoding='utf-8') as filely:
    meh = json.dumps(jdata, indent=4)
    filely.write(meh)
