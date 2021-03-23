# Dictionaries in Python are Mutable. Dictionaries are passed to functions by reference.

# A dictionary dict is declared as:

# dict={'Andrew':5, 'Brian':3, 'Clive':2, 'David':4}
# it contains the names of volunteers and the number of times that they have volunteered for a particular duty. The dictionary is regularly updated by providing both the dictionary and a list to a function upd.

# For the current update the following list has been declared - each name represents a new volunteer session:

# ulist = ['Brian', 'David', 'Peter']

# Write and demonstrate the function upd.

def upd(lis):

    for name in lis:
        # check if the name exists in the dict
        if name in udict:
            sessions = udict.get(name)
            sessions += 1
            udict[name] = sessions            
        else:
            udict[name] = 1


udict={'Andrew':5, 'Brian':3, 'Clive':2, 'David':4}
ulist = ['Brian', 'David', 'Peter']

upd(ulist)
