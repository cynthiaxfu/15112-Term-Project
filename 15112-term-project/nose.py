##############################################################################
# Name: Cynthia Fu
# AndrewID: cxfu
##############################################################################
# 15112 Term Project
# Nose Class
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
#Nose class - stores all nose images
class Nose(object):
    def __init__(self, mode):
        self.mode = mode
        self.nose1 = mode.loadImage('nose1.png')
        self.nose2 = mode.loadImage('nose2.png')
        self.nose3 = mode.loadImage('nose3.png')
        self.nose4 = mode.loadImage('nose4.png')
        self.nose5 = mode.loadImage('nose5.png')
        self.nose6 = mode.loadImage('nose6.png')
        self.nose7 = mode.loadImage('nose7.png')
        self.noseList = [self.nose1, self.nose2, self.nose3, self.nose4,
                         self.nose5, self.nose6, self.nose7]