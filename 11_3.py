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

db = dict()
