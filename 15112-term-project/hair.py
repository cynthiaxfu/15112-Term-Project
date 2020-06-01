##############################################################################
# Name: Cynthia Fu
# AndrewID: cxfu
##############################################################################
# 15112 Term Project
# Hair Class
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
#Hair class - stores all hair images
class Hair(object):
    def __init__(self, mode):
        self.mode = mode
        
        self.smallScale = 0.75
        self.largeScale = 0.9
        self.largeScale2 = 0.775
        self.hair1 = 'hair1Large.png'
        self.hair1Image = mode.scaleImage(mode.loadImage('hair1.png'),
                            self.smallScale)
        self.hair1Large = mode.scaleImage(mode.loadImage(self.hair1),
                            self.largeScale)
        self.hair2 = 'hair2Large.png'
        self.hair2Image = mode.scaleImage(mode.loadImage('hair2.png'),
                            self.smallScale)
        self.hair2Large = mode.scaleImage(mode.loadImage(self.hair2),
                            self.largeScale)
        self.hair3 = 'hair3Large.png'
        self.hair3Image = mode.scaleImage(mode.loadImage('hair3.png'),
                            self.smallScale)
        self.hair3Large = mode.scaleImage(mode.loadImage(self.hair3),
                            self.largeScale)
        self.hair4 = 'hair4Large.png'
        self.hair4Image = mode.scaleImage(mode.loadImage('hair4.png'),
                            self.smallScale)
        self.hair4Large = mode.scaleImage(mode.loadImage(self.hair4),
                            self.largeScale2)
        self.hair5 = 'hair5Large.png'
        self.hair5Image = mode.scaleImage(mode.loadImage('hair5.png'),
                            self.smallScale)
        self.hair5Large = mode.scaleImage(mode.loadImage(self.hair5),
                            self.smallScale)
        self.hair6 = 'hair6Large.png'
        self.hair6Image = mode.scaleImage(mode.loadImage('hair6.png'),
                            self.smallScale)
        self.hair6Large = mode.scaleImage(mode.loadImage(self.hair6),
                            self.largeScale)
        self.hair7 = 'hair7Large.png'
        self.hair7Image = mode.scaleImage(mode.loadImage('hair7.png'),
                            self.smallScale)
        self.hair7Large = mode.scaleImage(mode.loadImage(self.hair7),
                            self.largeScale2)
        
        self.hairListStrings = [self.hair1, self.hair2, self.hair3, self.hair4, 
                                self.hair5, self.hair6, self.hair7]
        self.hairList = [self.hair1Image, self.hair2Image, self.hair3Image, 
                         self.hair4Image, self.hair5Image, self.hair6Image,
                         self.hair7Image]
        self.hairLargeList = [self.hair1Large, self.hair2Large, self.hair3Large, 
                              self.hair4Large, self.hair5Large, self.hair6Large,
                              self.hair7Large]
        self.hairLargeScales = [self.largeScale, self.largeScale, 
                                self.largeScale, self.largeScale2, 
                                self.smallScale, self.largeScale, 
                                self.largeScale2]