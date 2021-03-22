""" is_leap takes a single year and returns True or False if the year is a leap year or not """
def is_leap(year):   
    result = False
    if year % 4 == 0:
        result = True
    elif year % 100 == 0:
        result = False
    elif year % 400 == 0:
        result = True
    return result

""" getLeapYearForRange takes 2 years and adds these to a dictionary.  The format is of the dictionary is year: True /False """
def getLeapYearForRange(year1, year2):

    # create the dictionary    
    leaps = {}

    # ensure we are working with ints
    year1 = int(year1)
    year2 = int(year2)

    # ensure that we have year 2 GREATER than year 1
    if year2 < year1:
        print("this is not valid.")
        exit
    
    # for loop to call the is_leap function and storing the result in a dictionary
    for x in range(year1, year2+1):
        res = is_leap(x)

        if res:
            print(x," is a leap year.")
            leaps[x] = res   
        else:
            print(x," is not a leap year.")
    return leaps

# ask for the years
year1 = input("Enter first year: ")
year2 = input("Enter second year: ")

# call the getLeapYearForRange function, passing in the years entered.
countOfLeaps = getLeapYearForRange(year1, year2)

# print out to the user how many leap years we have
print("There are ", len(countOfLeaps), "leap years in your range.")