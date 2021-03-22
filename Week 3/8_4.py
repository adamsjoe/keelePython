def encode_word(plaintext):
    saltPhrase = 'ABC'
    saltLen = len(saltPhrase)
    i = 0
    returnString = ''   

    for x in plaintext:
        if i < saltLen:  
            #plainVal = ord(x)         
            #saltVal = ord(saltPhrase[i])
            #saltedVal = plainVal + saltVal
            #print(plainVal)
            #print(saltVal)
            #print(saltedVal)
            returnVal = ord(x) + ord(saltPhrase[i])        
            returnString += chr(returnVal)
            i += 1
        else:
            i = 0            
            returnVal = ord(x)  + ord(saltPhrase[i])
            returnString += chr(returnVal)
    return returnString

def decode_word(secretText, saltPhrase):
    saltLen = len(saltPhrase)
    i = 0
    returnString = ''   

    for x in secretText:
        if i < saltLen:  
            #plainVal = ord(x)         
            #saltVal = ord(saltPhrase[i])
            #saltedVal = plainVal + saltVal
            #print(plainVal)
            #print(saltVal)
            #print(saltedVal)
            returnVal = ord(x) - ord(saltPhrase[i])        
            returnString += chr(returnVal)
            i += 1
        else:
            i = 0            
            returnVal = ord(x)  - ord(saltPhrase[i])
            returnString += chr(returnVal)
    return returnString

text = 'This is a secret'
ciper = encode_word(text)
print("Encrupted text is >>",ciper,"<<")
print("Plaintext is >>", decode_word(ciper, "ABC"), "<<")