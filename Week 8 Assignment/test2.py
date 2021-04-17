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
            json_file.write(jsonString)

    # handle file not found errors with a nice error message
    except FileNotFoundError:
        print('File {} does not exist.'.format(file_in))
        sys.exit(1)


def create2(file_in, file_out, headers=False):
    data = set()
    json_file = open(file_out, "w")

    with open(file_in, encoding='utf-8-sig', mode='r') as file:
        if headers is False:
            reader = csv.DictReader(file,)
        else:
            reader = csv.DictReader(file, fieldnames=headers)
        for row in reader:
            json.dump(row, json_file, indent=4)
            json_file.write("\n")
        
        #with open(file_out, 'w', encoding='utf-8') as json_file:
        #    jsonString = json.dumps(data, indent=4)            
        #    json_file.write(jsonString)            


#create2(MEMBERSFILE_CSV, MEMBERSFILE_JSON)
create_json(MEMBERSFILE_CSV, MEMBERSFILE_JSON)
