# Write a Python script to create and print a dictionary 
# where the keys are numbers between 1 and 15 (both included) and the values are cube of keys.

# create dictonary
theDict = {}
for x in range(1, 16):
    theDict[x] = x**3

print(theDict)