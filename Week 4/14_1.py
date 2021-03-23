# Copy and modify the above code to provide a function listext which takes a full path directory name and a file extension.
# 
#  It should recursively traverse all directories listing files with the specified extension. Provide a suitable docstring.

# def walk(dirname):
#     for name in os.listdir(dirname):
#         path = os.path.join(dirname, name)
#         if os.path.isfile(path):
#             print(path)
#         else:
#             walk(path)
        
# walk("Enter your own directory name")

import os

def listex(dirname, ext):
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            print(path)

list("C:\\Users\\Joseph")