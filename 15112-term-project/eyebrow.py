##############################################################################
# Name: Cynthia Fu
# AndrewID: cxfu
##############################################################################
# 15112 Term Project
# Eyebrow Class
##############################################################################
# Imports
##############################################################################
import module_manager
module_manager.review()
import cv2

from cmu_112_graphics import *
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
import math, copy, random
###############################################################################
# All images of facial features used in this project are from the online Mii 
# Studio created by Nintendo.
# This is an educational project and copyright infringement is not intended.
# Images used were also edited in Microsoft Word and Paint. 
###############################################################################
#Eyebrow class - stores all eyebrow coordinates
class Eyebrows(object):
    def __init__(self):
        #lines: startx, starty, endx, endy
        self.eyebrow1 = (0,0,50,0)
        self.eyebrow2 = (0,0,50,20)
        self.eyebrow3 = (0,0,60,30)

        #triangles: all coordinates
        self.eyebrow4 = (0,0,25,-25,50,0)
        self.eyebrow5 = (0,0,30,-25,25,0)
        self.eyebrow6 = (0,0,25,-30,50,-25)

        #lines with smooth: all coordinates
        self.eyebrow7 = (0,0,25,-25,50,0)
        self.eyebrow8 = (0,0,30,-25,40,0)
        self.eyebrow9 = (0,0,25,-50,40,-10)

        self.eyebrowList = [self.eyebrow1, self.eyebrow2, self.eyebrow3,
                            self.eyebrow4, self.eyebrow5, self.eyebrow6,
                            self.eyebrow7, self.eyebrow8, self.eyebrow9]