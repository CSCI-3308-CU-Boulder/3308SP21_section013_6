
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 2/16/21


import numpy as np
import cv2


print("Test!!!")

fabio_path = 'fabio.jpg'
lenna_path = 'lenna.png'

# Load Fabio in grayscale
fabio_gray = cv2.imread(fabio_path, 0)

# Load Lenna in grayscale
lenna_gray = cv2.imread(lenna_path, 0)

cv2.imshow('Fabio',fabio_gray)
cv2.imshow('Lenna',lenna_gray)

print("fabio_gray:\n.format{}", fabio_gray)
print("fabio_gray:\n.format{}", fabio_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()