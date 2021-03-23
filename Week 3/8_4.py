# A slightly more sophisticated form of cipher uses a shared phrase to determine the rotation of individual letters in a message. 
# Suppose our message was 'EFGH' and our shared phrase 'ABC'. For simplicity, lets keep everything to upper case and that within the 
# shared phrase A=1, B=2 and C=3. To encrypt we sequence through the message and the phrase simultaneously. 
# 
# Thus E is shifted by A (1). F is shifted by B (2). G is shifted by C (3). Finally, H is shifted by A (1) as we cycle around the shared phrase. 
# 
# Write a function that will accept a message and a phrase and encrypt it using this technique. Write a second function that will decrypt an encrypted message.
"""
Scramble takes 2 mandatory paramaters and 1 optional parameter.
This function can both code and decode a string based on a supplied key.
If the optional parameter is set to True, then the function will descramble the supplied text based on the key
"""
def scramble(plaintext, key, decode=False):
    # get the length of the saltphrase
    saltLen = len(key)
    
    # set up a counter
    i = 0
    
    # placeholder for the return string
    returnString = ''   

    # loop through each character in the plaintext
    for x in plaintext:

        # we need to loop the salt, so check if the counter is equal to the salt length
        if i < saltLen:      
            # either encode or decode the text based off the parameter.
            # as Strings are 0 based, we add 1 to get meet the requirement in the question
            if decode==True:
                returnVal = ord(x) - ord(str(i+1))            
            else:
                returnVal = ord(x) + ord(str(i+1))        
            # convert back to a char
            returnString += chr(returnVal)

            #increment counter
            i += 1
        else:
            i = 0            
            if decode==True:
                returnVal = ord(x)  - ord(str(i+1))
            else:
                returnVal = ord(x)  + ord(str(i+1))
            returnString += chr(returnVal)
    return returnString

# these are used a lot so make them vars
text = 'This is a test'
key = 'ABC'

# encrypt the text
ciper = scramble(text, key)

# print stuff to the user
print("Encrypted text is >>",ciper,"<<")
print("Plaintext is >>", scramble(ciper, key, True), "<<")