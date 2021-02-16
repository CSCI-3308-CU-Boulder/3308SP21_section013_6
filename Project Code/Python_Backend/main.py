
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 2/16/21


import numpy as np
import cv2


fabio_path = 'fabio.jpg'
lenna_path = 'lenna.png'

# Load Fabio in grayscale
fabio_color = cv2.imread(fabio_path)

# Load Lenna in grayscale
lenna_color = cv2.imread(lenna_path)

cv2.imshow('Fabio',fabio_color)
cv2.imshow('Lenna',lenna_color)

# Print pixel matrices for both images
# print("fabio_gray:\n{}\n", fabio_color)
# print("lenna_gray:\n{}\n", lenna_color)

cv2.waitKey(0)
cv2.destroyAllWindows()