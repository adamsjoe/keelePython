import csv


class LibraryMember(object):
    def __init__(self, id_no, first_name, last_name, gender, email, card_no):
        self.id_no = id_no
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.card_no = card_no


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


def sendEmail(addressee, subject, body):
    print("Sending email to '{}' with the subject '{}' and body '{}"
          .format(addressee, subject, body))


def checkInput(input, max_options):
    if input.isalpha:
        input = input.upper()
        

def mainMenu():
    print("**************************************")
    print("*            LIBRARY SYSTEM          *")
    print("**************************************")
    print("")
    print("")
    print("1) Member Details")
    print("")
    print("Q) Quit")
    print("")
    
    menu_option = input("Please select menu option: ")
    
    checkInput(menu_option, 1)
    

## main loop ##
# as this is a SYSTEM we could do a while loop and have a menu?
mainMenu()