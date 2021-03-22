# Exercise 8.3
# A Caesar cypher is a weak form of encryption that involves “rotating” each letter 
# by a fixed number of places. To rotate a letter means to shift it through the alphabet, 
# wrapping around to the beginning if necessary, so ’A’ rotated by 3 is ’D’ and ’Z’ rotated 
# by 1 is ’A’. To rotate a word, rotate each letter by the same amount. For example, “cheer” 
# rotated by 7 is “jolly” and “melon” rotated by -10 is “cubed”. In the movie 2001: A Space 
# Odyssey, the ship computer is called HAL, which is IBM rotated by -1.

def rotate_word(word, rotation):
    returnString = ''
    for x in word:
        returnVal = ord(x) + int(rotation)
        returnString += chr(returnVal)
    print(returnString)

secret = input('Enter your secret: ')
salt   = input('Enter your salt: ')
rotate_word(secret, salt)
