from PIL import Image
from PIL import Image
img=''

def call():
    s=3
    return(decrypt(decode(),s))



def decode():

    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3]]
        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def decrypt(string, shift):
        cipher = ''
        for char in string:
                if char == ' ':
                      cipher = cipher + char
                elif  char.isupper():
                      cipher = cipher + chr((ord(char) - shift - 65) % 26 + 65)
                else:
                      cipher = cipher + chr((ord(char) - shift - 97) % 26 + 97)

        return cipher
