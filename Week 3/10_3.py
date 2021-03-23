# Write a function called middle that takes a list and returns a new list that contains all but the first and last elements. For example:

# t = [1, 2, 3, 4]
# print(middle(t))

# [2, 3]

def middle(myList):
    # ignores the first and last entries
    newList = myList[1:-1]
    return newList

t = [1, 2, 3, 4]
print(middle(t))
