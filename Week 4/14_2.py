# In the resources folder for the module you will find a file txtsample.txt containg a simple text narrative from a children's book. 
# Download and save the file to either your Jupyter document directory or somewhere you can access it from Spyder. 
# Write a program to read the file, keeping tally of the frequency with which each unique word occurs (as a dictionary). 
# The file access should be protected in a try: block and any exception should lead to an explanatory message to the user.
#
# Write the dictionary to a file samplewords.json using the JSON format.

import json

filepathRead = 'sample.txt'
filepathWrite = 'samplewords.json'

uniqueWords = {}

def getval(x):
    global uniqueWords
    print(x)
    return uniqueWords[x]

try:
    with open(filepathRead, encoding="utf8") as file:
        # reading each line    
        for line in file:
    
            # reading each word        
            for word in line.split():
    
                # displaying the words           
                if word in uniqueWords:
                    instances = uniqueWords.get(word)
                    instances += 1
                    uniqueWords[word] =  instances
                else:
                    uniqueWords[word] =  1
except:
    print("issue")    

# sort the dictionary now
uniqueSorted = sorted(uniqueWords, key = getval) # wtf?!?!?!

try:
    with open(filepathWrite, 'w') as f:
        json.dump(uniqueWords, f)
except:
    print("blah")
    