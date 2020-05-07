# Use wave package (native to Python) for reading the received audio file
import wave
song1=''

def call():
    s=3
    return(decrypt(decode(),s))

def decode():
    song = wave.open(song1, mode='rb')
    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    return decoded
    song.close()


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
