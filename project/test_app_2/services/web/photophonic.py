
#--------------------------------------------------------
#
#
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 2/16/21
#
#
# Tones Docs: https://github.com/eriknyquist/tones
# OpenCV Docs: https://docs.opencv.org/master/index.html
#
#
#--------------------------------------------------------

import cv2

def theThing():
    return "wow it works. wak"

def getImageDimensions(filepath):
    print(filepath)
    mat = cv2.imread("project/static/" + filepath)
    if mat is None:
        return (0, 0)
    else:
        w = len(mat[0])
        h = len(mat)
        print(w)
        print(h)
        return (w, h)
