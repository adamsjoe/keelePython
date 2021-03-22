def encode_word(plaintext, saltPhrase):
    # get the length of the saltphrase
    saltLen = len(saltPhrase)
    
    # set up a counter
    i = 0
    
    # placeholder for the return string
    returnString = ''   

    # loop through each character in the plaintext
    for x in plaintext:

        # we need to loop the salt, so check if the counter is equal to the salt length
        if i < saltLen:  
            # convert the plantext char to numeric and the current salttext character and sum these
            returnVal = ord(x) + ord(saltPhrase[i])        
            # convert back to a char
            returnString += chr(returnVal)

            #increment counter
            i += 1
        else:
            i = 0            
            returnVal = ord(x)  + ord(saltPhrase[i])
            returnString += chr(returnVal)
    return returnString

# decode word is the same as encode, but subracting values, this could be made as one function with a paremeter
def decode_word(secretText, saltPhrase):
    saltLen = len(saltPhrase)
    i = 0
    returnString = ''   

    for x in secretText:
        if i < saltLen:  
            returnVal = ord(x) - ord(saltPhrase[i])        
            returnString += chr(returnVal)
            i += 1
        else:
            i = 0            
            returnVal = ord(x)  - ord(saltPhrase[i])
            returnString += chr(returnVal)
    return returnString

# these are used a lot so make them vars
text = 'This is a secret'
salt = 'ABC'

# encrypt the text
ciper = encode_word(text, salt)

# print stuff to the user
print("Encrypted text is >>",ciper,"<<")
print("Plaintext is >>", decode_word(ciper, salt), "<<")