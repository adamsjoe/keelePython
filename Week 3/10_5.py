# Write and test a function rem_dup that will remove duplicate items from a list. 
# It should return a new list without the duplicates in the old list. 
# 
# For example, rem_dup([1,2,2,3,4,6,6,8,1]) should return [1,2,3,4,6,8].

def rem_dup(myList):
    # create a set from the list
    # this will automatically remove duplicates
    return set(myList)

print(rem_dup([1,2,2,3,4,6,6,8,1]))