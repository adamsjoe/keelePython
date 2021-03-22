def is_leap(year):   
    result = False
    if year % 4 == 0:
        result = True
    elif year % 100 == 0:
        result = False
    elif year % 400 == 0:
        result = True
    return result

# get the years we are interested in
year1 = input("Enter first year: ")
year2 = input("Enter second year: ")

# convert to int
year1 = int(year1)
year2 = int(year2)

# handle folk being awkward
if year2 < year1:
    print("this is not valid.")
    exit

# we need to add 1 to the second parameter in range as this is not handled
for x in range(year1, year2+1):
    res = is_leap(x)

    if res:
        print(x," is a leap year.")
    else:
        print(x," is not a leap year.")