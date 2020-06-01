##############################################################################
# Name: Cynthia Fu
# AndrewID: cxfu
##############################################################################
# 15112 Term Project
# Face Class
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
#Face class - stores all face images
class Face(object):
    def __init__(self, mode):
        self.mode = mode
        self.scale = 1.2
        self.face1 = mode.loadImage('face1.png')
        self.face1Large = mode.scaleImage(mode.loadImage('face1large.png'), 
                            self.scale)
        self.face2 = mode.loadImage('face2.png')
        self.face2Large = mode.scaleImage(mode.loadImage('face2large.png'), 
                            self.scale)
        self.face3 = mode.loadImage('face3.png')   
        self.face3Large = mode.scaleImage(mode.loadImage('face3large.png'), 
                            self.scale)     
        self.face4 = mode.loadImage('face4.png')  
        self.face4Large = mode.scaleImage(mode.loadImage('face4large.png'), 
                            self.scale)    
        self.face5 = mode.loadImage('face5.png')
        self.face5Large = mode.scaleImage(mode.loadImage('face5large.png'), 
                            self.scale)

        self.faceList = [self.face1, self.face2, self.face3, self.face4, 
                         self.face5]
        self.faceLargeList = [self.face1Large, self.face2Large, self.face3Large,
                            self.face4Large, self.face5Large]