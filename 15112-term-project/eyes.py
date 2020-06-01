##############################################################################
# Name: Cynthia Fu
# AndrewID: cxfu
##############################################################################
# 15112 Term Project
# Eyes Class
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
#Eyes class - stores all eye images
class Eyes(object):
    def __init__(self, mode):
        self.mode = mode
        self.eye1 = mode.loadImage('eye1.png')
        self.eye2 = mode.loadImage('eye2.png')
        self.eye3 = mode.loadImage('eye3.png')
        self.eye4 = mode.loadImage('eye4.png')
        self.eye5 = mode.loadImage('eye5.png')
        self.eye6 = mode.loadImage('eye6.png')
        self.eye7 = mode.loadImage('eye7.png')
        self.eyeList = [self.eye1, self.eye2, self.eye3, self.eye4, self.eye5,
                        self.eye6, self.eye7]