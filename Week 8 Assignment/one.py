import sys
import csv


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

    def assignCardNo(self, new_card_no):
        self._card_no = new_card_no


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


members = open_file('members.csv', True)
print(type(members))

# convert the members to objects?
for line in members:
    memInstance = "member" + line[0]
    memInstance = LibraryMember(line[0],
                                line[1],
                                line[2],
                                line[3],
                                line[4],
                                line[5])

    # print(memInstance.printDetails())

