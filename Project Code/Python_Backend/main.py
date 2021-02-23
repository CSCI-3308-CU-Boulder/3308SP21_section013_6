
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 2/16/21


import numpy as np
import cv2

def isgray(imgpath):
    img = cv2.imread(imgpath)
    if len(img.shape) < 3: return True
    if img.shape[2]  == 1: return True
    b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
    if (b==g).all() and (b==r).all(): return True
    return False

def get_avg_colors(name, image, path):
    if isgray(path):
        print("\n ---- Analyzing {} in grayscale ---- ".format(name))
        mean = np.mean(image)
        max = np.max(image)
        min = np.min(image)
        print("Average value: {:.2f}".format(mean))
        print("Max value: {:.2f}".format(max))
        print("Min value: {:.2f}".format(min))
        print("Range of value: {:.2f}\n".format(max - min))
    else:
        print("\n ---- Analyzing {} in BGR color ---- ".format(name))
        blue = []
        green = []
        red = []
        count = 0
        pixel_sums = []
        for row in image:
            for pixel in row:
                count += 1
                blue.append(pixel[0])
                green.append(pixel[1])
                red.append(pixel[2])
                pixel_sums.append( ( (pixel[0]/3) + (pixel[1]/3) + (pixel[2]/3) ) )
        # print(pixel_sums)


        for color in [ [blue, "blue"], [green, "green"], [red, "red"] ]:
            mean = np.mean(color[0])
            max = np.max(color[0])
            min = np.min(color[0])
            print("Average {}: {:.2f}".format(color[1], mean))
            print("Max {}: {:.2f}".format(color[1], max))
            print("Min {}: {:.2f}".format(color[1], min))
            print("Range {}: {:.2f}\n".format(color[1], (max - min)) )

        avg_color = [np.sum(blue) / count, np.sum(green) / count, np.sum(red) / count]
        print("Average color value: [{:.2f}, {:.2f}, {:.2f}]".format(avg_color[0], avg_color[1], avg_color[2]))
        print("Range of color: {:.2f}".format( (np.max(pixel_sums)-np.min(pixel_sums)) )) # (a ratio of difference between colors)

        mean = np.mean(image)
        max = np.max(image)
        min = np.min(image)
        print("Average shade value: {:.2f}".format(mean))
        print("Max shade value: {:.2f}".format(max))
        print("Min shade value: {:.2f}".format(min))
        print("Range of shade value: {:.2f}\n".format(max - min))

fabio_path = 'fabio.jpg'
lenna_path = 'lenna.png'

# Load Fabio in grayscale
fabio_color = cv2.imread(fabio_path)

# Load Lenna in grayscale
lenna_color = cv2.imread(lenna_path)

get_avg_colors('Fabio', fabio_color, fabio_path)
get_avg_colors('Lenna', lenna_color, lenna_path)

# cv2.imshow('Fabio',fabio_color)
# cv2.imshow('Lenna',lenna_color)
# print("fabio_gray:\n{}\n", fabio_color)
# print("lenna_gray:\n{}\n", lenna_color)

cv2.waitKey(0)
cv2.destroyAllWindows()