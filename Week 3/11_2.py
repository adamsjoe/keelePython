# Write a Python program to create a dictionary from a string such that 
# each key is a unique letter from the string and the corresponding value is the number of times that the letter occurs in the string. 
# 
# So for the string "abracadabra" the dictionary should be {'a':5,'b':2,'c':1,'d':1,'r':2}

string = 'abracadabra'

data = dict()
for char in string:
    if char not in data:
        data[char] = 1
    else:
        data[char] += 1

print(data)