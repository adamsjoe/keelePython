import csv
import json
import pickle
from pprint import pprint

class LibraryMember(object):

    max_id = 0

    def __init__(self, id_no, first_name, last_name, gender, email, card_no):
        self._id_no = id_no
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._email = email
        self._card_no = card_no
        if self.max_id < int(id_no):
            self.max_id = int(id_no)

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

    def get_max_id(self):
        return self.max_id


filename = 'dogs'
outfile = open(filename, 'wb')

#
things = []
member = LibraryMember(1, 'Joseph', 'Adams', 'Male', 'joseph@random.com', 0)
member2 = LibraryMember(2, 'Joseph1', 'Adams1', 'Male', 'joseph@random.com1', 21)

things.append = member
things.append = member2

# jstr = json.dumps(member.__dict__)
jstr = json.dumps(member, default=vars)
jstr2 = json.dumps(member2, default=vars)

# things.append = jstr
# things.append = jstr2

# pickle.dump(member, outfile)
pprint(things)
# infile = open(filename, 'rb')

# new_dict = pickle.load(infile)

# infile.close()

# print(new_dict)