    while not menu_option:
        menu_option = input("You must enter an option")

def inputType():
    global menu_option        

def typeCheck():
    global menu_option
    try:
        float(menu_option) #First check for numeric. If this trips, program will move to except.
        if float(menu_option).is_integer() == True: #Checking if integer
            menu_option = 'an integer' 
        else:
            menu_option = 'a float' #Note: n.0 is considered an integer, not float
    except:
        if len(menu_option) == 1: #Strictly speaking, this is not really required. 
            if menu_option.isalpha() == True:
                menu_option = 'a letter'
            else:
                menu_option = 'a special character'
        else:
            inputLength = len(menu_option)
            if menu_option.isalpha() == True:
                menu_option = 'a character string of length ' + str(inputLength)
            elif menu_option.isalnum() == True:
                menu_option = 'an alphanumeric string of length ' + str(inputLength)
            else:
                menu_option = 'a string of length ' + str(inputLength) + ' with at least one special character'
    