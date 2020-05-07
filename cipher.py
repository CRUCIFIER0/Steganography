def encrypt(text):
    s=3
    result = "" 
  
    # traverse text 
    for i in range(len(text)): 
        char = text[i] 
  
        # Encrypt uppercase characters 
        if (char== " "):
            result += " "
            

  
        # Encrypt lowercase characters 
        elif(char.islower()): 
            result += chr((ord(char) + s - 97) % 26 + 97)

        else:
            result += chr((ord(char) + s-65) % 26 + 65)
             
             
  
    return result
def decrypt(text):
    s=3
    result = "" 
  
    # traverse text 
    for i in range(len(text)): 
        char = text[i] 
  
        # Encrypt uppercase characters 
        if (char==" "):
            result += " "
             
  
        # Encrypt lowercase characters 
        elif(char.islower()): 
            result += chr((ord(char) - s - 97) % 26 + 97)
        else:
            result += chr((ord(char) - s-65) % 26 + 65)
             
  
    return result

