import datetime

def getCurrentDaysExcelEpoch():
    f_date = datetime.date(1900, 1, 1)
    l_date = datetime.datetime.today().date()

    delta = l_date - f_date
    return delta.days


print(getCurrentDaysExcelEpoch())
print(type(getCurrentDaysExcelEpoch()))