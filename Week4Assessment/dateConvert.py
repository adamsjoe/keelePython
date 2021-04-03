import datetime


def convertEpochToReadable(dateIn):
    """Convert Excel Epoch time to a sting.



        Keyword arguments:
            dateIn -- the date (in excel epoch) format

        Returns:
            dateOut -- a date in string format (eg 12-01-1996)
    """
    # Mac and PC excel have different "start dates" - using a PC, but
    # leaving the mac code in if needed.
    EXCEL_DATE_SYSTEM_PC = 1900

    print(">> datetime.date: ", datetime.date(EXCEL_DATE_SYSTEM_PC, 1, 1))
    print(">> datetime.delta: ", datetime.timedelta(dateIn-2))
    dateOut = datetime.date(EXCEL_DATE_SYSTEM_PC, 1, 1) + datetime.timedelta(dateIn-2)
    print(dateOut)
    dateOut = dateOut.strftime("%d-%m-%Y")

    return dateOut


print(convertEpochToReadable(43490))