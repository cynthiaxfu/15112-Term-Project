##############################################################################
# Name: Cynthia Fu
# AndrewID: cxfu
##############################################################################
# 15112 Term Project
# Mouth Class
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
#Mouth class - stores all mouth images
class Mouth(object):
    def __init__(self, mode):
        self.mode = mode
        self.mouth1 = mode.loadImage('mouth1.png')
        self.mouth2 = mode.loadImage('mouth2.png')
        self.mouth3 = mode.loadImage('mouth3.png')
        self.mouth4 = mode.loadImage('mouth4.png')
        self.mouth5 = mode.loadImage('mouth5.png')
        self.mouth6 = mode.loadImage('mouth6.png')
        self.mouth7 = mode.loadImage('mouth7.png')
        self.mouthList = [self.mouth1, self.mouth2, self.mouth3, self.mouth4,
                            self.mouth5, self.mouth6, self.mouth7]
        self.startMouth = mode.loadImage('startMouth.png')
        self.startSmile = mode.loadImage('startSmile.png')
        self.startFrown = mode.loadImage('startFrown.png')
        self.smile = mode.loadImage('smile.png')
        self.frown = mode.loadImage('frown.png')
        self.mouthDict = {1: [self.startMouth, self.startSmile, 
                                self.smile, self.mouth1],
                          2: [self.startMouth, self.startSmile, 
                                self.smile, self.mouth2],
                          3: [self.startMouth, self.startFrown, 
                                self.frown, self.mouth3],
                          4: [self.startMouth, self.startSmile, 
                                self.smile, self.mouth4],
                          5: [self.startMouth, self.startSmile, 
                                self.smile, self.mouth5],
                          6: [self.startMouth, self.startFrown, 
                                self.frown, self.mouth6],
                          7: [self.startMouth, self.startFrown, 
                                self.frown, self.mouth7]}
