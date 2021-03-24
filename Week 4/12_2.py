# Write and demonstrate the use of a funtion getstats that accepts a Tuple of integer values as an argument 
# and returns a tuple with the Maximum, Minimum and Average value of the integers in the argument. For example, 
# the call could be:

# tup = getstats((33,44,55,66,77,23,43,54,65,88,12,34,23))

def getstats(t):
    average = 0
    for val in t:
        average = ave + val
    average = average / len(t)    
    return min(t), max(t), average

tup = getstats((33,44,55,66,77,23,43,54,65,88,12,34,23))
print(tup)
