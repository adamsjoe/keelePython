class Member(object):
    
    max_id = 0
    
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
        self._no_of_loaned_items = 0

    def printDetails(self):
        print("--> Member ID number   : ", self._id_no)
        print("--> Member First Name  : ", self._first_name)
        print("--> Member Last Name   : ", self._last_name)
        print("--> Member Gender      : ", self._gender)
        print("--> Member Email       : ", self._email)
        print("--> Member Card No     : ", self._card_no)
        print("--> Member Card Issue  : ", self._card_issue_no)
        print("--> No of items loaned : ", self._no_of_loaned_items)


class LibraryMember(Member):
    pass


mem = LibraryMember(1, "jo", "mas", "male", "email@me.com", "122")
mem1 = LibraryMember(2, "jo2", "mas2", "male", "email@me.com", "122")
mem2 = LibraryMember(None, "jo2", "mas2", "male", "email@me.com", "122")

print(mem.printDetails())
print(mem1.printDetails())
print(mem2.printDetails())
