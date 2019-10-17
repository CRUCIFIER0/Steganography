# Python program implementing Image Steganography
# PIL module is used to extract pixels of image and modify it
# pyfiglet is used for ASCII banner text
from PIL import Image
from pyfiglet import Figlet

############################### for text ########################################################3
# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                  imdata.__next__()[:3] +
                                  imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j]=='0') and (pix[j]% 2 != 0):

                if (pix[j]% 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Eigh^th pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def encode():
    img = input("Enter image name(with extension): ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of new image(with extension): ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
    img = input("Enter image name(with extension) :")
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
############################ for image ######################################################################
class Steganography(object):
    @staticmethod
    def __int_to_bin(rgb):
        """Convert an integer tuple to a binary (string) tuple.
        :param rgb: An integer tuple (e.g. (220, 110, 96))
        :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        """
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))

    @staticmethod
    def __bin_to_int(rgb):
        """Convert a binary (string) tuple to an integer tuple.
        :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :return: Return an int tuple (e.g. (220, 110, 96))
        """
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def __merge_rgb(rgb1, rgb2):
        """Merge two RGB tuples.
        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    @staticmethod
    def merge(img1, img2):
        """Merge two images. The second one will be merged into the first one.
        :param img1: First image
        :param img2: Second image
        :return: A new merged image.
        """

        # Check the images dimensions
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = Steganography.__int_to_bin((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = Steganography.__merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

        return new_image

    @staticmethod
    def unmerge(img):
        """Unmerge an image.
        :param img: The input image.
        :return: The unmerged/extracted image.
        """

        # Load the pixel map
        pixel_map = img.load()

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.__int_to_bin(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image


def merge():
    img1 = input("Enter image name(with extension): ")
    image1 = Image.open(img1, 'r')
    img2 = input("Enter image name(with extension): ")
    image2 = Image.open(img2, 'r')
    merged_image = Steganography.merge(image1,image2)
    new_img_name = input("Enter the name of new image(with extension): ")
    merged_image.save(new_img_name, str(new_img_name.split(".")[1].upper()))


def unmerge():
    img = input("Enter image name(with extension) :")
    image = Image.open(img, 'r')
    unmerged_image = Steganography.unmerge(image)
    new_img_name ="SecretMessage.PNG"
    unmerged_image.save(new_img_name, str(new_img_name.split(".")[1].upper()))
##################################### main method #########################################################################################
def main():
    custom_fig = Figlet(font='epic')
    print("###############$$$$$$$$$$$$$$################$$$$$$$$$$$$$$$############")
    print(custom_fig.renderText('Hello!! I Am  Stennar!!!'))
    print("###############$$$$$$$$$$$$$$################$$$$$$$$$$$$$$$############")
    print("What would you like to do today?")
    while(True):
        print("1.Work with Secret message and image")
        print("2.Work with Secret image and image")
        print("3.Exit")

        a= int(input("Enter your choice"))
        if (a == 1):
            print("1. Encode\n2. Decode\n")
            b= int(input("Enter your choice"))
            if (b==1):
                encode()
                print("Image has been successfully Encoded ")
                print("*********************************************************************")
                print()
                print("What would you like to do next ?")

            elif(b==2):
                print("Decoded word- " + decode())
                print("Image has been successfully Decoded ")
                print("*********************************************************************")
                print()
                print("What would you like to do next ?")
            else:
                raise Exception("Enter correct input")




        elif (a == 2):
            print("1. Encode\n2. Decode\n")
            b= int(input("Enter your choice"))
            if (b==1):
                merge()
                print("Image has been successfully Merged -Encoded ")
                print("*********************************************************************")
                print()
                print("What would you like to do next ?")
            elif(b==2):
                unmerge()
                print("Your file is saved as SecretMessage.PNG, please check your directory")
                print("Image has been successfully Demerged -Decoded ")
                print("*********************************************************************")
                print()
                print("What would you like to do next ?")
            else:
                raise Exception("Enter correct input")

        else:
            break



# Driver Code
if __name__ == '__main__' :
    print("*************************************************************************************************************************************")
    main()
    print("Thank you , have a nice day :)")
    print("*************************************************************************************************************************************")
