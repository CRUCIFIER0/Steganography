def read(file):
        with open(file,'r') as reader:
                return(reader.read())
        
def encrypt(string, shift):                         
        cipher = ''
        for char in string: 
                if char == ' ':
                      cipher = cipher + char
                elif  char.isupper():
                      cipher = cipher + chr((ord(char) + shift - 65) % 26 + 65)
                else:
                      cipher = cipher + chr((ord(char) + shift - 97) % 26 + 97)
  
        return cipher

 

def call(file):
        s = 3
        return(encrypt(read(file), s))

