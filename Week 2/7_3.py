def is_leap(year):   
    result = False
    if year % 4 == 0:
        result = True
    elif year % 100 == 0:
        result = False
    elif year % 400 == 0:
        result = True
    return result

stat = is_leap(2017)
print(stat)