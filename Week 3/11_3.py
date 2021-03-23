# Examine the following code:

# db=[
#   {
#     "name":"John",
#     "surname": "Davies",
#     "age": 23,
#     "company": {
#                      "name": "Google",
#                      "role": "Programmer"
#           }
#   },
#   {
#     "name":"Boris",
#     "surname": "Barry",
#     "age": 27,
#     "company": {
#                     "name": "Microsoft",
#                     "role": "Analysts"
#                }
#   },
#   {
#     "name":"Humphrey",
#     "surname": "Smith",
#     "age": 22,
#     "company": {
#                     "name": "Microsoft",
#                     "role": "Trainee programmer"
#                }
#   }
# ]
# Create a small program that lists all companies together with the full name of their employees. For example:

# Google : John Davies Microsoft : Boris Barry, Humphrey Smith

db=[
    {
        "name":"John",
        "surname": "Davies",
        "age": 23,
        "company": {
            "name": "Google",
            "role": "Programmer"
        }
    },
    {
        "name":"Boris",
        "surname": "Barry",
        "age": 27,
        "company": {
            "name": "Microsoft",
            "role": "Analysts"
            }
    },
    {
        "name":"Humphrey",
        "surname": "Smith",
        "age": 22,
        "company": {
            "name": "Microsoft",
            "role": "Trainee programmer"
            }
    }
]

# create a new dictionary
companies = {}
for i in db:
    # extract the name (first and surname)
    employeeName = i['name'] + ' ' + i['surname']
    # extract company
    employeeCompany= i['company']['name']

    # check if the company exists in the dictionary
    if employeeCompany in companies:
        # add the employee to the company and add a comma
        companies[employeeCompany] + ", " + employeeName
    else:
        companies[employeeCompany] = employeeName
    
print(companies)