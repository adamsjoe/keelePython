# Dictionaries in Python are Mutable. Dictionaries are passed to functions by reference.

# A dictionary dict is declared as:

# dict={'Andrew':5, 'Brian':3, 'Clive':2, 'David':4}
# it contains the names of volunteers and the number of times that they have volunteered for a particular duty. The dictionary is regularly updated by providing both the dictionary and a list to a function upd.

# For the current update the following list has been declared - each name represents a new volunteer session:

# ulist = ['Brian', 'David', 'Peter']

# Write and demonstrate the function upd.

def upd(lis):
    for name in lis:
        # check if the name (in the update list) exists in the dictionary
        if name in udict:
            # if the name exists, get the number of volunteering sessions the person has
            sessions = udict.get(name)
            # increment the sessions
            sessions += 1
            # write the new number of sessions back to the dictionary
            udict[name] = sessions            
        else:
            # the name doesn't exist, so we can set the volunteering sessions to 1
            udict[name] = 1


udict={'Andrew':5, 'Brian':3, 'Clive':2, 'David':4}
ulist = ['Brian', 'David', 'Peter']

# for information, print the dictionary before the update is performed
print(udict)

upd(ulist)

# print the dictionary after the update
print(udict)