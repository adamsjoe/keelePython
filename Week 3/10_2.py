# Write a function called cumsum that takes a list of numbers and returns the cumulative sum; that is, a new list where the ith element is the sum of the 
# first i + 1 elements from the original list. For example:

# t = [1, 2, 3]
# print(cumsum(t))

# [1, 3, 6]
# An empty list can be created with *newlist* = [] A list object's append() method can be used to add items to the end of a list.

def cumsum(theBiglist):
    """
    takes a list of integers
    returns a list of integers that is the cumulative sum of the previous integers
    """
    retLst = []
    cumulative = 0
    for number in theBiglist:
        cumulative += number
        retLst.append(cumulative)
    return retLst

t = [1, 2, 3]
print(cumsum(t))