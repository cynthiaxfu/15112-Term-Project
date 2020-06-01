##############################################################################
# Name: Cynthia Fu
# AndrewID: cxfu
##############################################################################
# 15112 Term Project
# Version 3
##############################################################################
# Changes in v3
#   More options for face and facial features
#   Skin Color 
#   Hair Color
#   Use a grid structure to position options for facial features
#   Drawing feature before export
#   User Input for number of sprites
#   
# Changes in v2
#   Added facial detection for face, nose, and mouth
#   Spritesheet can be exported using a screenshot
#
# Changes in v1
#   OOPy structure
#   Classes for Facial Features
#   Modal App Setup with modes for all facial features and screens
#   User can choose from 3 templates for all facial features
#   Facial detection using opencv option added for eyes
##############################################################################
# Imports
##############################################################################
import module_manager #from 112 website
module_manager.review()
import cv2
import numpy as np

from cmu_112_graphics import *
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
import math, copy, random
##############################################################################
# All images of facial features used in this project are from the online Mii 
# Studio created by Nintendo.
# This is an educational project and copyright infringement is not intended.
# Images used were also edited in Microsoft Word and Paint. 
##############################################################################
# Haar Cascades
##############################################################################
# included in opencv download
# from opencv/sources/data/haarcascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
# https://github.com/Itseez/opencv/blob/master 
# /data/haarcascades/haarcascade_eye.xml 
# Trained XML file for detecting eyes 
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/
# cascades/haarcascade_mcs_nose.xml
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
# https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/
# cascades/haarcascade_mcs_mouth.xml
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
###############################################################################
from face import *
from hair import *
from eyes import *
from eyebrow import *
from nose import *
from mouth import *
#####################################################################
# CMU 15112 Modal App Structure is an event-based animation framework
# from: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# file imported above as cmu_112_graphics
#####################################################################
class MyModalApp(ModalApp):
    #stores all modes of modal app
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.faceMode = FaceMode()
        app.hairMode = HairMode()
        app.eyeMode = EyeMode()
        app.eyebrowMode = EyebrowMode()
        app.noseMode = NoseMode()
        app.mouthMode = MouthMode()
        app.spriteSheetMode = SpriteSheetMode()
        app.exportSpriteSheetMode = ExportSpriteSheetMode()
        app.helpMode = HelpMode()
        app.exitMode = ExitMode()
        app.setActiveMode(app.splashScreenMode)

        app.previousMode = app.splashScreenMode

# start screen of modal app
class SplashScreenMode(Mode):

    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.setActiveMode(self.app.helpMode)
        else:
            self.app.setActiveMode(self.app.faceMode)
    
    def mousePressed(self, event):
        self.app.setActiveMode(self.app.faceMode)

    # draws text and instructions
    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/3, 
                            text = "Welcome to Emoji Spritesheet Maker!",
                            font = "Arial 22 bold")
        instructionsText = '''
        Instructions:
        Use the left and right arrow keys or 
        click to progress through the facial features.
        Click to select facial feature.
        Click on the camera icon to use your webcam 
        to take a picture and match the facial feature.
        If you need help, press 'h'.
        '''
        canvas.create_text(self.width/2, 2*self.height/3,
                            text = instructionsText,
                            font = "Arial 18 bold")
        canvas.create_text(self.width/2, self.height/2 - self.height/8,
                            text = "Click anywhere or press any key to start!",
                            font = "Arial 20 bold")

# help screen of modal app        
class HelpMode(Mode):
    # stores help text
    def appStarted(self):
        self.helpText = '''
        The left and right arrow keys allow you to scroll between the facial features
        Click on the options on the right side to select facial feature.
        The camera icon will allow you to use your webcam to take a picture, 
        and it will automatically match the facial feature with one of the templates.
        The mouth that is chosen will dictate the type of emotion the sprite will have.

        When exporting, follow directions on after selecting a mouth.

        Press 'h' or click anywhere to exit Help Mode.
        '''

    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.setActiveMode(self.app.previousMode)
    
    def mousePressed(self, event):
        self.app.setActiveMode(self.app.previousMode)

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/4, 
                            text = "Help",font = "Arial 24 bold" )
        canvas.create_text(self.width/2, self.height/2,
                           text = self.helpText, font = "Arial 14")

# select face screen
class FaceMode(Mode):

    #stores all features of face
    def appStarted(self):
        #from face class
        self.face = Face(self)
        self.faceList = self.face.faceList
        self.faceLargeList = self.face.faceLargeList

        self.faceListSizes = []
        self.maxFaceWidth = 0
        self.maxFaceHeight = 0
        for face in self.faceList:
            faceWidth, faceHeight = face.size
            self.faceListSizes.append((faceWidth, faceHeight))
            if faceWidth > self.maxFaceWidth:
                self.maxFaceWidth = faceWidth
            if faceHeight > self.maxFaceHeight:
                self.maxFaceHeight = faceHeight
        self.faceLargeListSizes = []
        for face in self.faceLargeList:
            faceWidth, faceHeight = face.size
            self.faceLargeListSizes.append((faceWidth, faceHeight))
        
        self.matchValues()

        #selected face
        self.savedFace = self.faceLargeList[0]
        self.savedWidth = self.faceLargeListSizes[0][0]
        self.savedHeight = self.faceLargeListSizes[0][1]

        self.graphicsAndButtons()

    #match values for face templates
    def matchValues(self):
        self.faceMatchValues = []
        for (width, height) in self.faceListSizes:
            matchValue = width*height
            self.faceMatchValues.append(matchValue)

    def graphicsAndButtons(self):    
        self.spacing = 100

        # camera button
        # image from: https://cdn.imgbin.com/15/10/3/
        # imgbin-computer-icons-camera-button-camera-xMMQ8LEXpsmqTPHj6tRdndC87.jpg
        self.cameraScale = 0.75
        self.cameraButton = self.scaleImage(self.loadImage('camerabutton.png'), 
                                            self.cameraScale)
        self.cameraButtonLocation = (7*self.width/8, 3*self.height/4)
        self.cameraButtonSize = self.cameraButton.size
        self.cameraText  = '''
        Click on the camera 
        to use your webcam
        '''
        #general buttons
        self.buttonWidth = 100
        self.buttonHeight = 50

        #selection buttons
        self.margin = 50
        self.selectionGridWidth = self.app.width//2 - 2*self.margin
        self.selectionGridHeight = self.app.height - 2*self.margin
        self.cols = self.selectionGridWidth // self.maxFaceWidth
        if len(self.faceList) % self.cols != 0:
            self.rows = len(self.faceList) // self.cols + 1
        else:
            self.rows = len(self.faceList) // self.cols
    
        self.buttonLocations = self.getButtonLocations()

        #skin color
        self.defaultColor = '#ffffff'
        self.skinColor = self.defaultColor
        self.selectedSkinColor = self.defaultColor

    #saves locations of face buttons
    def getButtonLocations(self):
        buttonLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cx = (x1+x0)/2
                cy = (y1+y0)/2
                buttonLocations.append((cx, cy))
                i+=1
                if i == len(self.faceList):
                    break
        return buttonLocations

    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + self.app.width/2 + col * self.maxFaceWidth
        x1 = self.margin + self.app.width/2 + (col+1) * self.maxFaceWidth
        y0 = self.margin + self.app.height/4 + row * self.maxFaceHeight
        y1 = self.margin + self.app.height/4 + (row+1) * self.maxFaceHeight
        return (x0, y0, x1, y1)

    def mousePressed(self, event):
        #buttons
        for i in range(len(self.buttonLocations)):
            if (event.y > self.buttonLocations[i][1] - self.faceListSizes[i][1]/2 and 
                event.y < self.buttonLocations[i][1] + self.faceListSizes[i][1]/2 and 
                event.x > self.buttonLocations[i][0] - self.faceListSizes[i][0]/2 and 
                event.x < self.buttonLocations[i][0]+ self.faceListSizes[i][0]/2):
                self.savedFace = self.faceLargeList[i]
                self.savedWidth = self.faceLargeListSizes[i][0]
                self.savedHeight = self.faceLargeListSizes[i][1]
                break
        #camera
        if (event.x > self.cameraButtonLocation[0] - self.cameraButtonSize[0]/2 and 
            event.x < self.cameraButtonLocation[0] + self.cameraButtonSize[0]/2 and 
            event.y > self.cameraButtonLocation[1] - self.cameraButtonSize[1]/2 and 
            event.y < self.cameraButtonLocation[1] + self.cameraButtonSize[1]/2):
            self.videoCapture()
            self.processImage()
            self.cameraText = "Face has been matched"
        #skin color
        elif (event.x > (5*self.width/8 - self.buttonWidth) and 
            event.x < (5*self.width/8 + self.buttonWidth) and 
            event.y > (3*self.height/4 - self.buttonHeight) and 
            event.y < (3*self.height/4 + self.buttonHeight)):
            self.selectedSkinColor = askcolor(color = self.selectedSkinColor)
            self.skinColor = self.selectedSkinColor[1]
            self.selectedSkinColor = self.defaultColor

    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.previousMode = self.app.faceMode
            self.app.setActiveMode(self.app.helpMode)
        elif event.key == "s":
            self.videoCapture()
            self.processImage()
            self.cameraText = "Face has been matched"
        elif (event.key == "Right"):
            self.app.setActiveMode(self.app.hairMode)
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.splashScreenMode)
        else:
            self.app.setActiveMode(self.app.hairMode)
    
    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/6, 
                            text = "Select a face", font = "Arial 24 bold")
        
        #camera
        canvas.create_text(3*self.width/4, 3*self.height/4 - self.spacing, 
                            text = self.cameraText, font = "Arial 14")
        canvas.create_image(7*self.width/8, 3*self.height/4, 
                            image = ImageTk.PhotoImage(self.cameraButton))
        
        #face buttons
        for i in range(len(self.faceList)):
            x,y = self.buttonLocations[i]
            canvas.create_image(x, y, 
                                image = ImageTk.PhotoImage(self.faceList[i]))
        
        #skin color button
        canvas.create_rectangle(5*self.width/8 - self.buttonWidth, 
                                3*self.height/4 - self.buttonHeight,
                                5*self.width/8 + self.buttonWidth, 
                                3*self.height/4 + self.buttonHeight,
                                fill = self.skinColor)
        #skin color text
        canvas.create_text(5*self.width/8, 
                           3*self.height/4,
                           text = "Select Skin Color")
        
        #skin color
        canvas.create_rectangle(self.width/2/2 - self.savedWidth/2, 
                                self.height/2 - self.savedHeight/2, 
                                self.width/2/2 + self.savedWidth/2, 
                                self.height/2 + self.savedHeight/2,
                                fill = self.skinColor)
        
        #face
        canvas.create_image(self.width/2/2, self.height/2, 
                    image = ImageTk.PhotoImage(self.savedFace))

    # uses opencv to capture face
    # modified from 
    # https://www.digitalocean.com/community/tutorials/
    # how-to-detect-and-extract-faces-from-an-image-with-opencv-and-python
    def videoCapture(self):
        # capture frames from webcam
        cap = cv2.VideoCapture(0)
        photoTaken = False
        
        # loop runs if capturing has been initialized 
        while 1:  
        
            # reads frames from webcam
            ret, img = cap.read()  
            # converts each frame to gray scale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
            # detects faces of different sizes in input image 
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        
            for (x,y,w,h) in faces: 
                # draw a rectangle around face  
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)  
                roi_gray = gray[y:y+h, x:x+w] 
                roi_color = img[y:y+h, x:x+w]

                #Make sure that there is only 1 face
                if (len(faces) == 1):
                    self.faceImg = faces[0]
                    cv2.imwrite(filename='saved_face.jpg', img=img)
                    photoTaken = True
                    break   
        
            # display an image in a window 
            cv2.imshow('img',img) 

            if photoTaken == True:
                break
        
            #Wait for Esc key to stop 
            k = cv2.waitKey(30) & 0xff
            if k == 27: 
                break
        
        # Close the window 
        cap.release() 
        
        # De-allocate any associated memory usage 
        cv2.destroyAllWindows() 
    
    #uses dimensions of face to match with face templates
    def processImage(self):
        self.faceWidth = self.faceImg[0]
        self.faceHeight = self.faceImg[1]
        matchValue = self.faceWidth * self.faceHeight

        lowDiffMatch = self.faceMatchValues[0]

        for i in range(len(self.faceMatchValues)):
            diff = abs(matchValue - self.faceMatchValues[i])
            if diff < lowDiffMatch:
                lowDiffMatch = diff
                self.savedFace = self.faceLargeList[i]
                self.savedWidth = self.faceLargeListSizes[i][0]
                self.savedHeight = self.faceLargeListSizes[i][1]

# select hair screen
class HairMode(Mode):
    #stores hair values
    def appStarted(self):
        #from Hair class
        self.hair = Hair(self)
        self.hairList = self.hair.hairList
        self.hairLargeList = self.hair.hairLargeList
        self.hairListStrings = self.hair.hairListStrings
        self.hairLargeScales = self.hair.hairLargeScales

        self.hairListSizes = []
        self.maxHairWidth = 0
        self.maxHairHeight = 0
        for hair in self.hairList:
            hairWidth, hairHeight = hair.size
            self.hairListSizes.append((hairWidth, hairHeight))
            if hairWidth > self.maxHairWidth:
                self.maxHairWidth = hairWidth
            if hairHeight > self.maxHairHeight:
                self.maxHairHeight = hairHeight

        self.savedHair = self.hairLargeList[0]
        self.spacing = 150

        self.graphicsAndButtons()

        #hair color
        self.hairColorRGB = (0,0,0)
        self.defaultColor = '#000000'
        self.hairColor = self.defaultColor
        self.selectedHairColor = self.defaultColor

    def graphicsAndButtons(self):
        #selection buttons
        self.margin = 50
        self.selectionGridWidth = self.app.width//2 - 2*self.margin
        self.selectionGridHeight = self.app.height - 2*self.margin
        self.cols = self.selectionGridWidth // self.maxHairWidth
        if len(self.hairList) % self.cols != 0:
            self.rows = len(self.hairList) // self.cols + 1
        else:
            self.rows = len(self.hairList) // self.cols
    
        self.buttonLocations = self.getButtonLocations()

        #general buttons
        self.buttonWidth = 100
        self.buttonHeight = 50

    #saves locations of hair buttons
    def getButtonLocations(self):
        buttonLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cx = (x1+x0)/2
                cy = (y1+y0)/2
                buttonLocations.append((cx, cy))
                i+=1
                if i == len(self.hairList):
                    break
        return buttonLocations

    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + self.app.width/2 + col * self.maxHairWidth
        x1 = self.margin + self.app.width/2 + (col+1) * self.maxHairWidth
        y0 = self.margin + self.app.height/4 + row * self.maxHairHeight
        y1 = self.margin + self.app.height/4 + (row+1) * self.maxHairHeight
        return (x0, y0, x1, y1)

    def mousePressed(self, event):

        #hair buttons
        for i in range(len(self.buttonLocations)):
            if (event.y > self.buttonLocations[i][1] - self.hairListSizes[i][1]/2 and 
                event.y < self.buttonLocations[i][1] + self.hairListSizes[i][1]/2 and 
                event.x > self.buttonLocations[i][0] - self.hairListSizes[i][0]/2 and 
                event.x < self.buttonLocations[i][0] + self.hairListSizes[i][0]/2):
                self.savedHair = self.hairLargeList[i]
                self.savedHairHeight = self.savedHair.size[1]
                break

        #change hair color
        if (event.x > (3*self.width/4 - self.buttonWidth) and 
            event.x < (3*self.width/4 + self.buttonWidth) and 
            event.y > (3*self.height/4 - self.buttonHeight) and 
            event.y < (3*self.height/4 + self.buttonHeight)):
            prevHairColor = self.selectedHairColor
            self.selectedHairColor = askcolor(color = self.selectedHairColor)
            if self.selectedHairColor != None:
                self.changeColor()
                self.hairColorRGB = self.selectedHairColor[0]
                self.hairColor = self.selectedHairColor[1]
                self.selectedHairColor = self.hairColor
            else: self.selectedHairColor = prevHairColor

    # modified from:
    # https://stackoverflow.com/questions/3752476/
    # python-pil-replace-a-single-rgba-color
    def changeColor(self):
        # when called self.hairColor is start
        # self.selectedHairColor is end
        r,g,b = self.hairColorRGB
        newR, newG, newB = self.selectedHairColor[0]
        start_color = (int(r), int(g), int(b), 0)
        new_color = (int(newR), int(newG), int(newB),255)
        
        for i in range(len(self.hairListStrings)):
            image = self.hairListStrings[i]
            # Open image
            shape_img = Image.open(image).convert('RGBA')
            shape_data = np.array(shape_img)

            data = np.array(shape_img)   # "data" is a height x width x 4 numpy array
            red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

            # Replace white with red... (leaves alpha values alone...)
            white_areas = (red == start_color[0]) & (blue == start_color[1]) & (green == start_color[2])
            data[..., :-1][white_areas.T] = new_color[:3] # Transpose back needed

            final_image = Image.fromarray(data)

            # Convert back to image
            imageName = f"hair{i+1}largecolored.png"
            final_image.save(imageName)
            self.hairLargeList[i] = self.scaleImage(final_image, 
                                        self.hairLargeScales[i])
    
    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.previousMode = self.app.hairMode
            self.app.setActiveMode(self.app.helpMode)
        elif event.key == "s":
            self.videoCapture()
            self.processImage()
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.faceMode)
        else:
            self.app.setActiveMode(self.app.eyeMode)

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/6, 
                            text = "Select a hairstyle",
                            font = "Arial 24 bold")  

        threefourths = 3/4 

        #change hair button        
        canvas.create_rectangle(threefourths*self.width - self.buttonWidth, 
                                threefourths*self.height - self.buttonHeight,
                                threefourths*self.width + self.buttonWidth, 
                                threefourths*self.height + self.buttonHeight,
                                fill = self.hairColor)

        canvas.create_text(threefourths*self.width, threefourths*self.height,
                           text = "Select Hair Color", fill = "white")
        
        #hair buttons
        for i in range(len(self.hairList)):
            x,y = self.buttonLocations[i]
            canvas.create_image(x, y, 
                                image = ImageTk.PhotoImage(self.hairList[i]))
        
        self.drawFacialFeatures(canvas)

    def drawFacialFeatures(self, canvas):
        #skin color
        canvas.create_rectangle(self.width/2/2 - self.app.faceMode.savedWidth/2, 
                                self.height/2 - self.app.faceMode.savedHeight/2, 
                                self.width/2/2 + self.app.faceMode.savedWidth/2, 
                                self.height/2 + self.app.faceMode.savedHeight/2,
                                fill = self.app.faceMode.skinColor)
        #face
        canvas.create_image(self.width/2/2, self.height/2, 
                    image = ImageTk.PhotoImage(self.app.faceMode.savedFace))

        #hair
        canvas.create_image(self.width/2/2, self.height/2, 
                            image = ImageTk.PhotoImage(self.savedHair))

# select eyes screen
class EyeMode(Mode):
    def appStarted(self):
        self.eyes = Eyes(self)
        self.eyesList = self.eyes.eyeList
        self.eyesListSizes = []
        self.maxEyeWidth = 0
        self.maxEyeHeight = 0
        for eyes in self.eyesList:
            eyesWidth, eyesHeight = eyes.size
            self.eyesListSizes.append((eyesWidth, eyesHeight))
            if eyesWidth > self.maxEyeWidth:
                self.maxEyeWidth = eyesWidth
            if eyesHeight > self.maxEyeHeight:
                self.maxEyeHeight = eyesHeight
        self.eyesMatchValues = []
        for (width, height) in self.eyesListSizes:
            matchValue = width*height
            self.eyesMatchValues.append(matchValue)

        self.savedEye = self.eyesList[0]
        self.savedEyeHeight = self.savedEye.size[1]
        self.spacing = 150
        
        self.eye1 = (-1,-1,-1,-1)
        self.eye2 = (-1,-1,-1,-1)

        self.graphicsAndButtons()

        #eye color
        self.defaultColor = '#000000'
        self.eyeColor = self.defaultColor
        self.selectedEyeColor = self.defaultColor

    def graphicsAndButtons(self): 
        # camera
        # image from: https://cdn.imgbin.com/15/10/3/
        # imgbin-computer-icons-camera-button-camera-xMMQ8LEXpsmqTPHj6tRdndC87.jpg
        self.cameraScale = 0.75
        self.cameraSpacing = 100
        self.cameraButton = self.scaleImage(self.loadImage('camerabutton.png'), 
                                            self.cameraScale)
        self.cameraButtonLocation = (7*self.width/8, 3*self.height/4)
        self.cameraButtonSize = self.cameraButton.size
        self.cameraText  = '''
        Click on the camera 
        to use your webcam
        '''

        #selection buttons
        self.margin = 50
        self.selectionGridWidth = self.app.width//2 - 2*self.margin
        self.selectionGridHeight = self.app.height - 2*self.margin
        self.cols = self.selectionGridWidth // self.maxEyeWidth
        if len(self.eyesList) % self.cols != 0:
            self.rows = len(self.eyesList) // self.cols + 1
        else:
            self.rows = len(self.eyesList) // self.cols
    
        self.buttonLocations = self.getButtonLocations()

        #general buttons
        self.buttonWidth = 100
        self.buttonHeight = 50

    #saves locations of eye buttons
    def getButtonLocations(self):
        buttonLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cx = (x1+x0)/2
                cy = (y1+y0)/2
                buttonLocations.append((cx, cy))
                i+=1
                if i == len(self.eyesList):
                    break
        return buttonLocations

    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + self.app.width/2 + col * self.maxEyeWidth
        x1 = self.margin + self.app.width/2 + (col+1) * self.maxEyeWidth
        y0 = self.margin + self.app.height/4 + row * self.maxEyeHeight
        y1 = self.margin + self.app.height/4 + (row+1) * self.maxEyeHeight
        return (x0, y0, x1, y1)

    def mousePressed(self, event):
        #eye buttons
        for i in range(len(self.buttonLocations)):
            if (event.y > self.buttonLocations[i][1] - self.eyesListSizes[i][1] and 
                event.y < self.buttonLocations[i][1] + self.eyesListSizes[i][1] and 
                event.x > self.buttonLocations[i][0] - self.eyesListSizes[i][0] and 
                event.x < self.buttonLocations[i][0] + self.eyesListSizes[i][0]):
                self.savedEye = self.eyesList[i]
                self.savedEyeHeight = self.savedEye.size[1]
                break
        #camera button
        if (event.y > self.cameraButtonLocation[1] - self.cameraButtonSize[1] and 
            event.y < self.cameraButtonLocation[1] + self.cameraButtonSize[1] and 
            event.x > self.cameraButtonLocation[0] - self.cameraButtonSize[0] and 
            event.x < self.cameraButtonLocation[0] + self.cameraButtonSize[0]):
            self.videoCapture()
            self.processImage()
            self.cameraText = "Eye has been matched"
        #change eye color
        elif (event.x > (5*self.width/8 - self.buttonWidth) and 
            event.x < (5*self.width/8 + self.buttonWidth) and 
            event.y > (3*self.height/4 - self.buttonHeight) and 
            event.y < (3*self.height/4 + self.buttonHeight)):
            self.selectedEyeColor = askcolor(color = self.selectedEyeColor)
            self.eyeColor = self.selectedEyeColor[1]
            self.selectedEyeColor = self.defaultColor
        
    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.previousMode = self.app.eyeMode
            self.app.setActiveMode(self.app.helpMode)
        elif event.key == "s":
            self.videoCapture()
            self.processImage()
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.hairMode)
        elif (event.key == "Right"):
            self.app.setActiveMode(self.app.eyebrowMode)
        else:
            self.app.setActiveMode(self.app.eyebrowMode)

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/6, text = "Select an eye",
                            font = "Arial 24 bold")      
        #camera
        canvas.create_text(3*self.width/4, 3*self.height/4 - self.cameraSpacing, 
                            text = self.cameraText, font = "Arial 14")
        canvas.create_image(7*self.width/8, 3*self.height/4, 
                            image = ImageTk.PhotoImage(self.cameraButton))
        #eye color button
        canvas.create_rectangle(5*self.width/8 - self.buttonWidth, 
                                3*self.height/4 - self.buttonHeight,
                                5*self.width/8 + self.buttonWidth, 
                                3*self.height/4 + self.buttonHeight,
                                fill = self.eyeColor)

        canvas.create_text(5*self.width/8, 3*self.height/4,
                           text = "Select Eye Color", fill = "white")
        
        self.drawFacialFeatures(canvas)

    def drawFacialFeatures(self, canvas):
        #skin color
        canvas.create_rectangle(self.width/2/2 - self.app.faceMode.savedWidth/2, 
                                self.height/2 - self.app.faceMode.savedHeight/2, 
                                self.width/2/2 + self.app.faceMode.savedWidth/2, 
                                self.height/2 + self.app.faceMode.savedHeight/2,
                                fill = self.app.faceMode.skinColor)

        #face
        canvas.create_image(self.width/4, self.height/2, 
                    image = ImageTk.PhotoImage(self.app.faceMode.savedFace))

        #matches eye in list
        for i in range(len(self.eyesList)):
            x,y = self.buttonLocations[i]
            canvas.create_image(x, y, 
                                image = ImageTk.PhotoImage(self.eyesList[i]))

        #draws eye color
        radius = self.savedEyeHeight/2 - 10*2
        canvas.create_oval(self.width/4 + self.spacing/3 - radius, 
                            self.height/2 - self.spacing/4 - radius,
                            self.width/4 + self.spacing/3 + radius, 
                            self.height/2 - self.spacing/4 + radius,
                            fill = self.eyeColor,outline = self.eyeColor)
        canvas.create_oval(self.width/4 - self.spacing/3 - radius, 
                            self.height/2 - self.spacing/4 - radius,
                            self.width/4 - self.spacing/3 + radius, 
                            self.height/2 - self.spacing/4 + radius,
                            fill = self.eyeColor,outline = self.eyeColor)

        #draws eyes
        savedEye2 = self.savedEye.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.create_image(self.width/4 + self.spacing/3, self.height/2 - self.spacing/4,
                                image = ImageTk.PhotoImage(self.savedEye))
        canvas.create_image(self.width/4 - self.spacing/3, self.height/2 - self.spacing/4,
                                image = ImageTk.PhotoImage(savedEye2))
        
        #hair
        canvas.create_image(self.width/2/2, self.height/2, 
                        image = ImageTk.PhotoImage(self.app.hairMode.savedHair))

    # uses opencv to allow user to take image of own eyes
    # modified from 
    # https://www.digitalocean.com/community/tutorials/
    # how-to-detect-and-extract-faces-from-an-image-with-opencv-and-python
    def videoCapture(self):
        # capture frames from webcam 
        cap = cv2.VideoCapture(0)
        photoTaken = False
        
        # loop runs if capturing has been initialized 
        while 1:  
        
            # reads frames from webcam
            ret, img = cap.read()  
            # converts each frame to gray scale 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
            # detects faces of different sizes in the input image 
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        
            for (x,y,w,h) in faces: 
                # draws rectangle around face 
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)  
                roi_gray = gray[y:y+h, x:x+w] 
                roi_color = img[y:y+h, x:x+w] 
        
                # detects eyes of different sizes in the input image 
                eyes = eye_cascade.detectMultiScale(roi_gray)  
        
                # draws rectangle around eyes 
                for (ex,ey,ew,eh) in eyes: 
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)  
                
                # make sure that there is only 1 face and 2 eyes in the face
                if ((len(faces) == 1) and (len(eyes) == 2)):
                    self.eye1 = eyes[0]
                    self.eye2 = eyes[1]
                    cv2.imwrite(filename='saved_eyes.jpg', img=img)
                    photoTaken = True
                    break   

            # display image in a window 
            cv2.imshow('img',img) 
            
            # exits when face and eyes are detected
            if photoTaken == True:
                break
        
            # Wait for Esc key to stop 
            k = cv2.waitKey(30) & 0xff
            if k == 27: 
                break
        
        # Close the window 
        cap.release() 
        
        # De-allocate any associated memory usage 
        cv2.destroyAllWindows() 
    
    #processes dimensions taken from the image retrieved in 
    def processImage(self):
        self.eye1Width = self.eye1[0]
        self.eye1Height = self.eye1[1]
        matchValue = self.eye1Width * self.eye1Height

        lowDiffMatch = self.eyesMatchValues[0]
        for i in range(len(self.eyesMatchValues)):
            diff = abs(matchValue - self.eyesMatchValues[i])
            if diff < lowDiffMatch:
                lowDiffMatch = diff
                self.savedEye = self.eyesList[i]

# select eyebrows screen
class EyebrowMode(Mode):
    def appStarted(self):
        self.eyebrowObject = Eyebrows()
        self.eyebrowList = self.eyebrowObject.eyebrowList

        self.maxEyebrowWidth = 0
        self.maxEyebrowHeight = 0
        for eyebrow in self.eyebrowList:
            for i in range(len(eyebrow)):
                if i % 2 == 0:
                    if eyebrow[i] > self.maxEyebrowWidth:
                        self.maxEyebrowWidth = eyebrow[i] * 2
                else:
                    if eyebrow[i] > self.maxEyebrowHeight:
                        self.maxEyebrowHeight = eyebrow[i] * 5

        self.savedEyebrow = self.eyebrowList[0]
        self.savedEyebrowIndex = 0

        self.graphicsAndButtons()

        self.defaultColor = "#000000"
        self.eyebrowColor = self.defaultColor
        self.selectedEyebrowColor = self.defaultColor
        self.spacing = 50

    def graphicsAndButtons(self):
        #selection buttons
        self.margin = 50
        self.selectionGridWidth = self.app.width//2 - 2*self.margin
        self.selectionGridHeight = self.app.height - 2*self.margin
        self.cols = self.selectionGridWidth // self.maxEyebrowWidth
        if len(self.eyebrowList) % self.cols != 0:
            self.rows = len(self.eyebrowList) // self.cols + 1
        else:
            self.rows = len(self.eyebrowList) // self.cols
    
        self.buttonLocations = self.getButtonLocations()

        #general buttons
        self.buttonWidth = 100
        self.buttonHeight = 50

    # gets coordinates of the opposite eyebrow 
    # because all eyebrow coordinates are for the eyebrow on the right side
    def getOtherEyebrow(self, eyebrow):
        otherEyebrow = []
        for i in range(len(eyebrow)):
            if i % 2 == 0:
                otherEyebrow.append(-eyebrow[i])
            else:
                otherEyebrow.append(eyebrow[i])
        return (otherEyebrow)

    # draws eyebrow on canvas
    def drawCanvasEyebrow(self, canvas, index, cx, cy):
        # 1-3 are lines - index 0 to 2
        # 4-6 are triangles - index 3 to 5
        # 7-8 are lines with smooth/arcs - index 6 to 7

        if index <= 2:
            x0, y0, x1, y1 = self.eyebrowList[index]
            canvas.create_line(cx + x0, cy + y0, cx + x1, cy + y1, 
                                fill = self.eyebrowColor, width = 5)
        elif index <= 5:
            x0, y0, x1, y1, x2, y2 = self.eyebrowList[index]
            canvas.create_polygon(cx + x0, cy + y0, cx + x1, cy + y1, 
                                  cx + x2, cy + y2, fill = self.eyebrowColor)
        else:
            x0, y0, x1, y1, x2, y2 = self.eyebrowList[index]
            canvas.create_line(cx + x0, cy + y0, cx + x1, cy + y1, 
                               cx + x2, cy + y2, fill = self.eyebrowColor, 
                               smooth = 1, width = 5)

    #draws other eyebrow on canvas
    def drawOtherEyebrow(self, canvas, index, cx, cy, eyebrow):
        if index <= 2:
            x0, y0, x1, y1 = eyebrow
            canvas.create_line(cx + x0, cy + y0, cx + x1, cy + y1, 
                                fill = self.eyebrowColor, width = 5)
        elif index <= 5:
            x0, y0, x1, y1, x2, y2 = eyebrow
            canvas.create_polygon(cx + x0, cy + y0, cx + x1, cy + y1, 
                                  cx + x2, cy + y2, fill = self.eyebrowColor)
        else:
            x0, y0, x1, y1, x2, y2 = eyebrow
            canvas.create_line(cx + x0, cy + y0, cx + x1, cy + y1, 
                               cx + x2, cy + y2, fill = self.eyebrowColor, 
                               smooth = 1, width = 5)

    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + self.app.width/2 + col * self.maxEyebrowWidth
        x1 = self.margin + self.app.width/2 + (col+1) * self.maxEyebrowWidth
        y0 = self.margin + self.app.height/3 + row * self.maxEyebrowHeight
        y1 = self.margin + self.app.height/3 + (row+1) * self.maxEyebrowHeight
        return (x0, y0, x1, y1)
    
    #saves locations of eyebrow buttons
    def getButtonLocations(self):
        buttonLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cx = (x1+x0)//2
                cy = (y1+y0)//2
                buttonLocations.append((cx, cy))
                i+=1
                if i == len(self.eyebrowList):
                    break
        return buttonLocations

    # user can change modes and launch camera using keys
    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.previousMode = self.app.eyebrowMode
            self.app.setActiveMode(self.app.helpMode)
        elif event.key == "s":
            self.videoCapture()
            self.processImage()
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.eyeMode)
        elif (event.key == "Right"):
            self.app.setActiveMode(self.app.noseMode)
    
    # user can select eyebrows, launch camera, and change color using mouse
    def mousePressed(self, event):
        #buttons
        for i in range(len(self.buttonLocations)):
            if (event.x > self.buttonLocations[i][0] - self.maxEyebrowWidth/2 and 
                event.x < self.buttonLocations[i][0] + self.maxEyebrowWidth/2 and 
                event.y > self.buttonLocations[i][1] - self.maxEyebrowHeight/2 and 
                event.y < self.buttonLocations[i][1] + self.maxEyebrowHeight/2):
                self.savedEyebrow = self.eyebrowList[i]
                self.savedEyebrowIndex = i
                break
        #eyebrow color
        if (event.x > (3*self.width/4 - self.buttonWidth) and 
            event.x < (3*self.width/4 + self.buttonWidth) and 
            event.y > (3*self.height/4 - self.buttonHeight) and 
            event.y < (3*self.height/4 + self.buttonHeight)):
            self.selectedEyebrowColor = askcolor(color = self.selectedEyebrowColor)
            self.eyebrowColor = self.selectedEyebrowColor[1]
            self.selectedEyebrowColor = self.defaultColor

    #draws all features in app
    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/6, text = "Select an eyebrow",
                            font = "Arial 24 bold")

        self.drawFacialFeatures(canvas)

        #color button
        canvas.create_rectangle(3*self.width/4 - self.buttonWidth, 
                                3*self.height/4 - self.buttonHeight,
                                3*self.width/4 + self.buttonWidth, 
                                3*self.height/4 + self.buttonHeight,
                                fill = self.eyebrowColor)

        canvas.create_text(3*self.width/4, 
                           3*self.height/4,
                           text = "Select Eyebrow Color",
                           fill = "white")
        
        #draw eyebrow button locations
        for i in range(len(self.eyebrowList)):
            x,y = self.buttonLocations[i]
            self.drawCanvasEyebrow(canvas,i,x,y)

    def drawFacialFeatures(self, canvas):
        #skin color
        canvas.create_rectangle(self.width/2/2 - self.app.faceMode.savedWidth/2, 
                                self.height/2 - self.app.faceMode.savedHeight/2, 
                                self.width/2/2 + self.app.faceMode.savedWidth/2, 
                                self.height/2 + self.app.faceMode.savedHeight/2,
                                fill = self.app.faceMode.skinColor)
        #face
        canvas.create_image(self.width/4, self.height/2, 
                    image = ImageTk.PhotoImage(self.app.faceMode.savedFace))
        
        #eye color
        radius = self.app.eyeMode.savedEyeHeight/2 - 10*2
        canvas.create_oval(self.width/4 + self.app.eyeMode.spacing/3 - radius, 
                            self.height/2 - self.app.eyeMode.spacing/4 - radius,
                            self.width/4 + self.app.eyeMode.spacing/3 + radius, 
                            self.height/2 - self.app.eyeMode.spacing/4 + radius,
                            fill = self.app.eyeMode.eyeColor,
                            outline = self.app.eyeMode.eyeColor)
        canvas.create_oval(self.width/4 - self.app.eyeMode.spacing/3 - radius, 
                            self.height/2 - self.app.eyeMode.spacing/4 - radius,
                            self.width/4 - self.app.eyeMode.spacing/3 + radius, 
                            self.height/2 - self.app.eyeMode.spacing/4 + radius,
                            fill = self.app.eyeMode.eyeColor,
                            outline = self.app.eyeMode.eyeColor)
        
        #eyes
        savedEye2 = self.app.eyeMode.savedEye.transpose(Image.FLIP_LEFT_RIGHT)
        eyeSpacing = 150
        canvas.create_image(self.width/4 + eyeSpacing/3, self.height/2 - eyeSpacing/4,
                                image = ImageTk.PhotoImage(self.app.eyeMode.savedEye))
        canvas.create_image(self.width/4 - eyeSpacing/3, self.height/2 - eyeSpacing/4,
                                image = ImageTk.PhotoImage(savedEye2))

        #eyebrows
        eyebrow2 = self.getOtherEyebrow(self.savedEyebrow)
        cx = self.width/4 + eyeSpacing/6
        cy = self.height/2 - eyeSpacing/5 - self.spacing
        self.drawCanvasEyebrow(canvas,self.savedEyebrowIndex, cx, cy)
        self.drawOtherEyebrow(canvas, self.savedEyebrowIndex, 
                                cx - self.spacing, cy, eyebrow2)
        
        #hair
        canvas.create_image(self.width/2/2, self.height/2, 
                        image = ImageTk.PhotoImage(self.app.hairMode.savedHair))
        
# select nose screen
class NoseMode(Mode):
    #stores nose 
    def appStarted(self):
        #from class
        self.nose = Nose(self)
        self.noseList = self.nose.noseList

        self.noseListSizes = []
        self.maxNoseWidth = 0
        self.maxNoseHeight = 0
        for nose in self.noseList:
            noseWidth, noseHeight = nose.size
            self.noseListSizes.append((noseWidth, noseHeight))
            if noseWidth > self.maxNoseWidth:
                self.maxNoseWidth = noseWidth
            if noseHeight > self.maxNoseHeight:
                self.maxNoseHeight = noseHeight
        
        #match values for nose templates
        self.noseMatchValues = []
        for (width, height) in self.noseListSizes:
            matchValue = width * height
            self.noseMatchValues.append(matchValue)

        self.savedNose = self.noseList[0]
        self.spacing = 150
        self.graphicsAndButtons()

    def graphicsAndButtons(self):
        # camera button
        # image from: https://cdn.imgbin.com/15/10/3/
        # imgbin-computer-icons-camera-button-camera-xMMQ8LEXpsmqTPHj6tRdndC87.jpg
        self.cameraScale = 0.75
        self.cameraButton = self.scaleImage(self.loadImage('camerabutton.png'), 
                                            self.cameraScale)
        self.cameraButtonLocation = (3*self.width/4, 3*self.height/4)
        self.cameraButtonSize = self.cameraButton.size
        self.cameraText  = '''
        Click on the camera 
        to use your webcam
        '''

        #selection buttons
        self.margin = 50
        self.selectionGridWidth = self.app.width//2 - 2*self.margin
        self.selectionGridHeight = self.app.height - 2*self.margin
        self.cols = self.selectionGridWidth // self.maxNoseWidth
        if len(self.noseList) % self.cols != 0:
            self.rows = len(self.noseList) // self.cols + 1
        else:
            self.rows = len(self.noseList) // self.cols
    
        self.buttonLocations = self.getButtonLocations()

    #saves locations of nose buttons
    def getButtonLocations(self):
        buttonLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cx = (x1+x0)/2
                cy = (y1+y0)/2
                buttonLocations.append((cx, cy))
                i+=1
                if i == len(self.noseList):
                    break
        return buttonLocations

    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + self.app.width/2 + col * self.maxNoseWidth
        x1 = self.margin + self.app.width/2 + (col+1) * self.maxNoseWidth
        y0 = self.margin + self.app.height/4 + row * self.maxNoseHeight
        y1 = self.margin + self.app.height/4 + (row+1) * self.maxNoseHeight
        return (x0, y0, x1, y1)

    def mousePressed(self, event):
        #nose buttons
        for i in range(len(self.buttonLocations)):
            if (event.y > self.buttonLocations[i][1] - self.noseListSizes[i][1] and 
                event.y < self.buttonLocations[i][1] + self.noseListSizes[i][1] and 
                event.x > self.buttonLocations[i][0] - self.noseListSizes[i][0] and 
                event.x < self.buttonLocations[i][0]+ self.noseListSizes[i][0]):
                self.savedNose = self.noseList[i]
                break
        #camera
        if (event.y > self.cameraButtonLocation[1] - self.cameraButtonSize[1] and 
            event.y < self.cameraButtonLocation[1] + self.cameraButtonSize[1] and 
            event.x > self.cameraButtonLocation[0] - self.cameraButtonSize[0] and 
            event.x < self.cameraButtonLocation[0] + self.cameraButtonSize[0]):
            self.videoCapture()
            self.processImage()
            self.cameraText = "Nose has been matched"

    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.previousMode = self.app.noseMode
            self.app.setActiveMode(self.app.helpMode)
        elif event.key == "s":
            self.videoCapture()
            self.processImage()
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.eyebrowMode)
        else:
            self.app.setActiveMode(self.app.mouthMode)

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/5, 
                            text = "Select a nose", font = "Arial 24 bold")
        
        #camera
        canvas.create_text(3*self.width/4, 3*self.height/4 - self.spacing, 
                            text = self.cameraText, font = "Arial 14")
        canvas.create_image(3*self.width/4, 3*self.height/4, 
                            image = ImageTk.PhotoImage(self.cameraButton))
        
        #buttons
        for i in range(len(self.noseList)):
            x,y = self.buttonLocations[i]
            canvas.create_image(x, y, 
                                image = ImageTk.PhotoImage(self.noseList[i]))
        
        self.drawFacialFeatures(canvas)

    def drawFacialFeatures(self, canvas):
        #skin color
        canvas.create_rectangle(self.width/2/2 - self.app.faceMode.savedWidth/2, 
                                self.height/2 - self.app.faceMode.savedHeight/2, 
                                self.width/2/2 + self.app.faceMode.savedWidth/2, 
                                self.height/2 + self.app.faceMode.savedHeight/2,
                                fill = self.app.faceMode.skinColor)
        #face
        canvas.create_image(self.width/4, self.height/2, 
                    image = ImageTk.PhotoImage(self.app.faceMode.savedFace))
        
        #eye color
        radius = self.app.eyeMode.savedEyeHeight/2 - 10*2
        canvas.create_oval(self.width/4 + self.spacing/3 - radius, 
                            self.height/2 - self.spacing/4 - radius,
                            self.width/4 + self.spacing/3 + radius, 
                            self.height/2 - self.spacing/4 + radius,
                            fill = self.app.eyeMode.eyeColor,
                            outline = self.app.eyeMode.eyeColor)
        canvas.create_oval(self.width/4 - self.spacing/3 - radius, 
                            self.height/2 - self.spacing/4 - radius,
                            self.width/4 - self.spacing/3 + radius, 
                            self.height/2 - self.spacing/4 + radius,
                            fill = self.app.eyeMode.eyeColor,
                            outline = self.app.eyeMode.eyeColor)
        
        #eyes
        savedEye1 = self.app.eyeMode.savedEye
        savedEye2 = savedEye1.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.create_image(self.width/4 + self.spacing/3, 
                            self.height/2 - self.spacing/4,
                            image = ImageTk.PhotoImage(savedEye1))
        canvas.create_image(self.width/4 - self.spacing/3, 
                            self.height/2 - self.spacing/4,
                            image = ImageTk.PhotoImage(savedEye2))
        
        #eyebrows
        eyeSpacing = self.spacing
        eyebrow1 = self.app.eyebrowMode.savedEyebrow
        eyebrow2 = self.app.eyebrowMode.getOtherEyebrow(eyebrow1)
        cx = self.width/4 + eyeSpacing/6
        cy = self.height/2 - eyeSpacing/5 - self.app.eyebrowMode.spacing
        self.app.eyebrowMode.drawCanvasEyebrow(canvas,
                        self.app.eyebrowMode.savedEyebrowIndex, cx, cy)
        self.app.eyebrowMode.drawOtherEyebrow(canvas, 
                                self.app.eyebrowMode.savedEyebrowIndex, 
                                cx - self.app.eyebrowMode.spacing, cy, eyebrow2)
        #nose
        canvas.create_image(self.width/4, self.height/2, 
                            image = ImageTk.PhotoImage(self.savedNose))
        
        #hair
        canvas.create_image(self.width/2/2, self.height/2, 
                        image = ImageTk.PhotoImage(self.app.hairMode.savedHair))
    
    # uses opencv to allow user to take image of own nose
    # modified from 
    # https://www.digitalocean.com/community/tutorials/
    # how-to-detect-and-extract-faces-from-an-image-with-opencv-and-python
    def videoCapture(self):
        # capture frames from webcam
        cap = cv2.VideoCapture(0)
        photoTaken = False
        
        # loop runs if capturing has been initialized
        while 1:  
        
            # reads frames from webcam
            ret, img = cap.read()  
            # converts each frame to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
            # detects faces of different sizes in the input image 
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        
            # draws rectangles around faces
            for (x,y,w,h) in faces:   
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)  
                roi_gray = gray[y:y+h, x:x+w] 
                roi_color = img[y:y+h, x:x+w] 
        
                # detects noses of different sizes in the input image 
                noses = nose_cascade.detectMultiScale(roi_gray)  
        
                # draws rectangle around nose in face
                for (nx,ny,nw,nh) in noses: 
                    cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(0,255,0),2)  

                #Make sure that there is only 1 face and 1 nose in the face
                if ((len(faces) == 1) and (len(noses) == 1)):
                    self.noseImg = noses[0]
                    cv2.imwrite(filename='saved_Nose.jpg', img=img)
                    photoTaken = True
                    break   
        
            # Display an image in a window 
            cv2.imshow('img',img) 

            if photoTaken == True:
                break
        
            #Wait for Esc key to stop 
            k = cv2.waitKey(30) & 0xff
            if k == 27: 
                break
        
        # Close the window 
        cap.release() 
        
        # De-allocate any associated memory usage 
        cv2.destroyAllWindows() 

    #processes dimensions taken from the image retrieved in
    def processImage(self):
        widthIndex = 2
        heightIndex = 3
        self.noseWidth = self.noseImg[widthIndex]
        self.noseHeight = self.noseImg[heightIndex]
        matchValue = self.noseWidth / self.noseHeight

        lowDiffMatch = self.noseMatchValues[0]
        for i in range(len(self.noseMatchValues)):
            diff = abs(matchValue - self.noseMatchValues[i])
            if diff < lowDiffMatch:
                lowDiffMatch = diff
                self.savedNose = self.noseList[i]

# select mouth screen
class MouthMode(Mode):
    def appStarted(self):
        #from Mouth class
        self.mouth = Mouth(self)
        self.mouthList = self.mouth.mouthList

        self.mouthListSizes = []
        self.maxMouthWidth = 0
        self.maxMouthHeight = 0
        for mouth in self.mouthList:
            mouthWidth, mouthHeight = mouth.size
            self.mouthListSizes.append((mouthWidth, mouthHeight))
            if mouthWidth > self.maxMouthWidth:
                self.maxMouthWidth = mouthWidth
            if mouthHeight > self.maxMouthHeight:
                self.maxMouthHeight = mouthHeight

        self.mouthText = '''
        The mouth will determine the sprite's expression.
        Present mouth and selected mouths will be on spritesheet
        '''

        #match values of mouth templates
        self.mouthMatchValues = []
        for (width, height) in self.mouthListSizes:
            matchValue = width*height
            self.mouthMatchValues.append(matchValue)
        self.savedMouth = self.mouthList[0]
        self.spacing = 150

        self.graphicsAndButtons()

        self.selectedMouths = []
        self.fill = "white"
        self.fillList = [self.fill, self.fill, self.fill, self.fill, self.fill,
                         self.fill, self.fill]
        
    def graphicsAndButtons(self):
        # camera button
        # image from: https://cdn.imgbin.com/15/10/3/
        # imgbin-computer-icons-camera-button-camera-xMMQ8LEXpsmqTPHj6tRdndC87.jpg
        self.cameraScale = 0.75
        self.cameraButton = self.scaleImage(self.loadImage('camerabutton.png'), 
                                            self.cameraScale)
        self.cameraButtonLocation = (7*self.width/8, 3*self.height/4)
        self.cameraButtonSize = self.cameraButton.size
        self.cameraText  = '''
        Click on the camera 
        to use your webcam
        '''

        #selection buttons
        self.margin = 50
        self.selectionGridWidth = self.app.width//2 - 2*self.margin
        self.selectionGridHeight = self.app.height - 2*self.margin
        self.cols = self.selectionGridWidth // self.maxMouthWidth
        if len(self.mouthList) % self.cols != 0:
            self.rows = len(self.mouthList) // self.cols + 1
        else:
            self.rows = len(self.mouthList) // self.cols
    
        self.buttonLocations = self.getButtonLocations()

        self.checkBoxGridWidth = self.app.width//2 -2*self.margin
        self.checkBoxGridHeight = self.app.height//2//2 - 2*self.margin
        self.checkCols = 2
        self.checkRows = len(self.mouthList)

        self.checkBoxWidth = self.checkBoxGridWidth // self.checkRows
        self.checkBoxHeight = self.checkBoxGridHeight // self.checkCols

        self.checkBoxLocations = self.getCheckBoxLocations()

    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids    
    def getCheckBoxBounds(self, row, col):
        threeFourths = 5/8
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + self.app.width/2 + col * self.checkBoxWidth
        x1 = self.margin + self.app.width/2 + (col+1) * self.checkBoxWidth
        y0 = (self.margin + self.app.height * threeFourths 
                    + row * self.checkBoxHeight)
        y1 = (self.margin + self.app.height* threeFourths + 
                    (row+1) * self.checkBoxHeight)
        return (x0, y0, x1, y1)

    #saves locations of mouth buttons
    def getCheckBoxLocations(self):
        checkBoxLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCheckBoxBounds(row, col)
                cx = (x1+x0)/2
                cy = (y1+y0)/2
                checkBoxLocations.append((cx, cy))
                i+=1
                if i == len(self.mouthList):
                    break
        return checkBoxLocations

    #saves locations of mouth buttons
    def getButtonLocations(self):
        buttonLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cx = (x1+x0)/2
                cy = (y1+y0)/2
                buttonLocations.append((cx, cy))
                i+=1
                if i == len(self.mouthList):
                    break
        return buttonLocations

    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + self.app.width/2 + col * self.maxMouthWidth
        x1 = self.margin + self.app.width/2 + (col+1) * self.maxMouthWidth
        y0 = self.margin + self.app.height/4 + row * self.maxMouthHeight
        y1 = self.margin + self.app.height/4 + (row+1) * self.maxMouthHeight
        return (x0, y0, x1, y1)

    def mousePressed(self, event):
        #mouth buttons
        for i in range(len(self.buttonLocations)):
            if (event.y > self.buttonLocations[i][1] - self.mouthListSizes[i][1] and 
                event.y < self.buttonLocations[i][1] + self.mouthListSizes[i][1] and 
                event.x > self.buttonLocations[i][0] - self.mouthListSizes[i][0] and 
                event.x < self.buttonLocations[i][0] + self.mouthListSizes[i][0]):
                self.savedMouth = self.mouthList[i]
                if len(self.selectedMouths) <= 1:
                    self.selectedMouths = [self.mouthList[i]]
                else:
                    self.selectedMouths.append(self.mouthList[i])
                break
        #box buttons
        for i in range(len(self.checkBoxLocations)):
            if (event.y > self.checkBoxLocations[i][1] - self.checkBoxHeight/2 and 
                event.y < self.checkBoxLocations[i][1] + self.checkBoxHeight/2 and 
                event.x > self.checkBoxLocations[i][0] - self.checkBoxWidth/2 and 
                event.x < self.checkBoxLocations[i][0] + self.checkBoxWidth/2):
                if self.fillList[i] == "red":
                    self.fillList[i] = "white"
                    self.selectedMouths.remove(self.mouthList[i])
                else:
                    self.fillList[i] = "red"
                    self.selectedMouths.append(self.mouthList[i])
                break
        #camera
        if (event.y > self.cameraButtonLocation[1] - self.cameraButtonSize[1] and 
            event.y < self.cameraButtonLocation[1] + self.cameraButtonSize[1] and 
            event.x > self.cameraButtonLocation[0] - self.cameraButtonSize[0] and 
            event.x < self.cameraButtonLocation[0] + self.cameraButtonSize[0]):
            self.videoCapture()
            self.processImage()
            self.cameraText = "Mouth has been matched"

    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.previousMode = self.app.mouthMode
            self.app.setActiveMode(self.app.helpMode)
        elif event.key == "s":
            self.videoCapture()
            self.processImage()
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.noseMode)
        else:
            self.app.setActiveMode(self.app.exportSpriteSheetMode)
    
    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/5, 
                            text = "Select a mouth", font = "Arial 24 bold")
        canvas.create_text(self.width/4, 7*self.height/8, 
                            text = self.mouthText, font = "Arial 12")

        #camera
        canvas.create_text(3*self.width/4, 3*self.height/4 - self.spacing, 
                            text = self.cameraText, font = "Arial 14")
        canvas.create_image(7*self.width/8, 3*self.height/4, 
                            image = ImageTk.PhotoImage(self.cameraButton))
        
        #mouth buttons
        for i in range(len(self.mouthList)):
            x,y = self.buttonLocations[i]
            canvas.create_image(x, y, 
                                image = ImageTk.PhotoImage(self.mouthList[i]))
            canvas.create_rectangle(x - self.maxMouthWidth/2, 
                                    y - self.maxMouthHeight/2,
                                    x + self.maxMouthWidth/2, 
                                    y + self.maxMouthHeight/2)
        #box buttons
        for i in range(len(self.mouthList)):
            x,y = self.checkBoxLocations[i]
            canvas.create_rectangle(x - self.checkBoxWidth/2, 
                                    y - self.checkBoxHeight/2,
                                    x + self.checkBoxWidth/2, 
                                    y + self.checkBoxHeight/2,
                                    fill = self.fillList[i])
            canvas.create_text(x,y,text = f"mouth{i}")

        self.drawFacialFeatures(canvas)

    def drawFacialFeatures(self, canvas):
        #skin color
        canvas.create_rectangle(self.width/2/2 - self.app.faceMode.savedWidth/2, 
                                self.height/2 - self.app.faceMode.savedHeight/2, 
                                self.width/2/2 + self.app.faceMode.savedWidth/2, 
                                self.height/2 + self.app.faceMode.savedHeight/2,
                                fill = self.app.faceMode.skinColor)
        
        #face
        canvas.create_image(self.width/4, self.height/2, 
                    image = ImageTk.PhotoImage(self.app.faceMode.savedFace))

        #eye color
        radius = self.app.eyeMode.savedEyeHeight/2 - 10*2
        canvas.create_oval(self.width/4 + self.spacing/3 - radius, 
                            self.height/2 - self.spacing/4 - radius,
                            self.width/4 + self.spacing/3 + radius, 
                            self.height/2 - self.spacing/4 + radius,
                            fill = self.app.eyeMode.eyeColor,
                            outline = self.app.eyeMode.eyeColor)
        canvas.create_oval(self.width/4 - self.spacing/3 - radius, 
                            self.height/2 - self.spacing/4 - radius,
                            self.width/4 - self.spacing/3 + radius, 
                            self.height/2 - self.spacing/4 + radius,
                            fill = self.app.eyeMode.eyeColor,
                            outline = self.app.eyeMode.eyeColor)
        
        #eyes
        savedEye1 = self.app.eyeMode.savedEye
        savedEye2 = savedEye1.transpose(Image.FLIP_LEFT_RIGHT)
        canvas.create_image(self.width/4 + self.spacing/3, 
                            self.height/2 - self.spacing/4,
                            image = ImageTk.PhotoImage(savedEye1))
        canvas.create_image(self.width/4 - self.spacing/3, 
                            self.height/2 - self.spacing/4,
                            image = ImageTk.PhotoImage(savedEye2))
        
        #eyebrows
        eyeSpacing = self.spacing
        eyebrow1 = self.app.eyebrowMode.savedEyebrow
        eyebrow2 = self.app.eyebrowMode.getOtherEyebrow(eyebrow1)
        cx = self.width/4 + eyeSpacing/6
        cy = self.height/2 - eyeSpacing/5 - self.app.eyebrowMode.spacing
        self.app.eyebrowMode.drawCanvasEyebrow(canvas,
                        self.app.eyebrowMode.savedEyebrowIndex, cx, cy)
        self.app.eyebrowMode.drawOtherEyebrow(canvas, 
                                self.app.eyebrowMode.savedEyebrowIndex, 
                                cx - self.app.eyebrowMode.spacing, cy, eyebrow2)
        #nose
        canvas.create_image(self.width/4, self.height/2, 
                image = ImageTk.PhotoImage(self.app.noseMode.savedNose))
        
        spacing = 70 #between nose and mouth

        #mouth
        canvas.create_image(self.width/4, self.height/2 + spacing, 
                    image = ImageTk.PhotoImage(self.savedMouth))
        
        #hair
        canvas.create_image(self.width/2/2, self.height/2, 
                        image = ImageTk.PhotoImage(self.app.hairMode.savedHair))
    
    # uses opencv to allow user to take image of mouth
    # modified from 
    # https://www.digitalocean.com/community/tutorials/
    # how-to-detect-and-extract-faces-from-an-image-with-opencv-and-python
    def videoCapture(self):
        # capture frames from a camera 
        cap = cv2.VideoCapture(0)
        photoTaken = False
        
        # loop runs if capturing has been initialized. 
        while 1:  
        
            # reads frames from a camera 
            ret, img = cap.read()  
            # convert to gray scale of each frames 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
            # Detects faces of different sizes in the input image 
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        
            for (x,y,w,h) in faces: 
                # To draw a rectangle in a face  
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)  
                roi_gray = gray[y:y+h, x:x+w] 
                roi_color = img[y:y+h, x:x+w]
        
                # Detects mouths of different sizes in the input image 
                mouths = mouth_cascade.detectMultiScale(roi_gray)  
        
                #To draw a rectangle around mouth
                for (mx,my,mw,mh) in mouths: 
                    cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,255,0),2)  

                #Make sure that there is only 1 face and 1 mouth in the face
                if ((len(faces) == 1) and (len(mouths) == 1)):
                    self.mouthImg = mouths[0]
                    # need to check locations of mouth
                    cv2.imwrite(filename='saved_Mouth.jpg', img=img)
                    photoTaken = True
                    break
        
            # Display an image in a window 
            cv2.imshow('img',img) 

            if photoTaken == True:
                break
        
            #Wait for Esc key to stop 
            k = cv2.waitKey(30) & 0xff
            if k == 27: 
                break
        
        # Close the window 
        cap.release() 
        
        # De-allocate any associated memory usage 
        cv2.destroyAllWindows() 
    
    #processes dimensions of image to match with mouth templates
    def processImage(self):
        widthIndex = 2
        heightIndex = 3
        self.mouthWidth = self.mouthImg[widthIndex]
        self.mouthHeight = self.mouthImg[heightIndex]
        matchValue = self.mouthWidth*2 * self.mouthHeight
        lowDiffMatch = self.mouthMatchValues[0]
        for i in range(len(self.mouthMatchValues)):
            diff = abs(matchValue - self.mouthMatchValues[i])
            if diff < lowDiffMatch:
                lowDiffMatch = diff
                self.savedMouth = self.mouthList[i]

#instructions and editing options to generate spritesheet
class ExportSpriteSheetMode(Mode):
    def appStarted(self):
        self.numSprites = 4
        self.defaultNumSprites = 4

        self.colorButtonWidth = 100
        self.colorButtonHeight = 50
        
        self.numSpritesButtonWidth = 150
        self.numSpritesButtonHeight = 50
        
        self.defaultColor = "#000000"
        self.color = self.defaultColor
        self.selectedColor = self.defaultColor

        self.message = "Press u to update values when viewing spritesheet"

    def keyPressed(self, event):
        if (event.key == "Right"):
            self.app.previousMode = self.app.exportSpriteSheetMode
            self.app.setActiveMode(self.app.spriteSheetMode)
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.mouthMode)
        elif (event.key == "Space"):
            self.app.setActiveMode(self.app.exitMode)

    def mousePressed(self, event):
        # UserInput modified from: 
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        if (event.x > self.width/4 - self.numSpritesButtonWidth and 
           event.x < self.width/4 + self.numSpritesButtonWidth and 
           event.y > 3*self.height/4 - self.numSpritesButtonHeight and
           event.y < 3*self.height/4 + self.numSpritesButtonHeight):
            self.numSprites = self.getUserInput('Enter a number from 1 to 4')
            if (self.numSprites == None):
                self.numSprites = 4
            else:
                self.numSprites = int(self.numSprites)
                if(self.numSprites > self.defaultNumSprites 
                            or self.numSprites < 1):
                    self.message = f'''
                    That is an invalid number. 
                    The number of sprites has been restored to {self.defaultNumSprites}
                    '''
                else:
                    self.message = "Press u to update values when viewing spritesheet"
        #pen color
        elif (event.x > 3*self.width/4 - self.colorButtonWidth and 
           event.x < 3*self.width/4 + self.colorButtonWidth and 
           event.y > 3*self.height/4 - self.colorButtonHeight and
           event.y < 3*self.height/4 + self.colorButtonHeight):
            self.selectedColor = askcolor(color = self.selectedColor)
            self.color = self.selectedColor[1]
            self.selectedColor = self.defaultColor

    def redrawAll(self, canvas):
        #uses screenshot shortcut from cmu_112_graphics.py
        exportInstructions = '''
        Generating your spritesheet...

        Press the right arrow key to view spritesheet and 
        then use control-s to screenshot spritesheet

        If you go back and edit any feature, press u to update spritesheet.

        To edit the spritesheet, drag mouse to draw.
        To change color, click the button below.
        Press d to delete last stroke

        Press left arrow key after screenshot to return to this page
        Press space to exit
        '''
        canvas.create_text(self.width/2, self.height/3, 
                            text = exportInstructions,
                            font = "Arial 16 bold")
        
        canvas.create_rectangle(self.width/4 - self.numSpritesButtonWidth,
                                3*self.height/4 - self.numSpritesButtonHeight,
                                self.width/4 + self.numSpritesButtonWidth,
                                3*self.height/4 + self.numSpritesButtonHeight)
        
        canvas.create_text(self.width/4, 3*self.height/4, 
                            text = "Select number of sprites wanted")
        
        canvas.create_text(self.width/4, 
                           3*self.height/4 + self.numSpritesButtonHeight*2,
                           text = self.message)

        canvas.create_rectangle(3*self.width/4 - self.colorButtonWidth,
                                3*self.height/4 - self.colorButtonHeight,
                                3*self.width/4 + self.colorButtonWidth,
                                3*self.height/4 + self.colorButtonHeight)
        
        canvas.create_text(3*self.width/4, 3*self.height/4, 
                            text = "Change Pen Color")

#spritesheet to export
class SpriteSheetMode(Mode):
    def appStarted(self):
        #drawing lists
        self.strokeList = []
        self.pixelList = []

        self.faceAttributes()

    def faceAttributes(self):
        self.selectedMouths = []
        for mouth in self.app.mouthMode.selectedMouths:
            self.mouthsList = self.app.mouthMode.mouth.mouthList    
            index = -1
            for i in range(len(self.mouthsList)):
                if mouth == self.mouthsList[i]:
                    index = i+1
                    self.selectedMouths.append(index)
        self.selectedMouths = set(self.selectedMouths)

        #eye spacing
        self.spacing = 150
        #create grid
        self.scale = 1
        # calculate how many faces can fit width wise and height wise
        # adjust scale accordingly
        self.defaultNumSprites = 4
        self.spritesPerMouth = self.app.exportSpriteSheetMode.numSprites
        self.numSprites = len(self.selectedMouths) * self.spritesPerMouth
        self.faceWidth = self.app.faceMode.savedWidth
        self.faceHeight = self.app.faceMode.savedHeight
        self.spriteWidth = self.faceWidth
        self.spriteHeight = self.faceHeight
        if self.faceWidth * self.numSprites > self.app.width:
            self.spriteWidth = self.app.width//self.numSprites
            self.scale = self.spriteWidth/self.faceWidth
            self.spriteHeight = self.faceHeight * self.scale    
            self.spacing *= self.scale
        
        self.face = self.scaleImage(self.app.faceMode.savedFace, self.scale)
        self.rightEye = self.scaleImage(self.app.eyeMode.savedEye, self.scale)
        savedEye2 = self.app.eyeMode.savedEye.transpose(Image.FLIP_LEFT_RIGHT)
        self.leftEye = self.scaleImage(savedEye2,self.scale)
        self.nose = self.scaleImage(self.app.noseMode.savedNose, self.scale)
        self.hair = self.scaleImage(self.app.hairMode.savedHair, self.scale)

        self.margin = 50
        self.spriteSheetWidth = self.app.width - 2*self.margin
        self.spriteSheetHeight = self.app.height - 2*self.margin
        self.cols = self.spriteSheetWidth // self.spriteWidth

        self.spriteMouthList = []

        for i in self.selectedMouths:
            copyList = copy.deepcopy(self.app.mouthMode.mouth.mouthDict[i])
            copySpriteMouthList = copy.deepcopy(copyList)
            if len(copyList) != self.spritesPerMouth:
                sliceIndex = abs(len(copySpriteMouthList)-self.spritesPerMouth)
                copyList = self.app.mouthMode.mouth.mouthDict[i]
                newSpriteMouthList = copyList[sliceIndex:]
                copyList = newSpriteMouthList
            
            for index in range(len(copyList)):
                self.spriteMouthList.append(copyList[index])

        if len(self.spriteMouthList) % self.cols != 0:
            self.rows = len(self.spriteMouthList) // self.cols + 1
        else:
            self.rows = len(self.spriteMouthList) // self.cols
        
        self.spriteLocations = self.getSpriteLocations()
    
    def getSpriteLocations(self):
        spriteLocations = []
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                cx = (x1+x0)/2
                cy = (y1+y0)/2
                spriteLocations.append((cx, cy))
                i+=1
                if i == len(self.spriteMouthList):
                    break
        return spriteLocations
    
    # modified from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        #grid is on the right side, starting at self.app.height/3
        x0 = self.margin + col * self.spriteWidth
        x1 = self.margin + (col+1) * self.spriteWidth
        y0 = self.margin + row * self.spriteHeight
        y1 = self.margin + (row+1) * self.spriteHeight
        return (x0, y0, x1, y1)
    
    def keyPressed(self, event):
        if (event.key == "h"):
            self.app.previousMode = self.app.SpriteSheetMode
            self.app.setActiveMode(self.app.helpMode)
        elif (event.key == "Left"):
            self.app.setActiveMode(self.app.exportSpriteSheetMode)
        elif (event.key == "Right" or event.key == "Space"):
            self.app.setActiveMode(self.app.exitMode)
        elif (event.key == "u"):
            self.faceAttributes()
        elif(event.key == "d"):
            self.strokeList.pop()

    def mousePressed(self, event):
        #detects draw
        self.pixelList.append((event.x, event.y))
    
    def mouseDragged(self, event):
        #draws
        self.pixelList.append((event.x, event.y))

    def mouseReleased(self, event):
        self.strokeList.append(self.pixelList)
        self.pixelList = []

    def redrawAll(self, canvas):
        for i in range(len(self.spriteMouthList)):
            cx,cy = self.spriteLocations[i]

            #skin color
            canvas.create_rectangle(cx - self.spriteWidth/2, 
                                cy - self.spriteHeight/2, 
                                cx + self.spriteWidth/2, 
                                cy + self.spriteHeight/2,
                                fill = self.app.faceMode.skinColor)

            #face
            canvas.create_image(cx, cy, 
                        image = ImageTk.PhotoImage(self.face))
            
            #eye color
            radius = (self.app.eyeMode.savedEyeHeight/2 - 10*2) * self.scale
            canvas.create_oval(cx + self.spacing/3 - radius, 
                                cy - self.spacing/4 - radius,
                                cx + self.spacing/3 + radius, 
                                cy - self.spacing/4 + radius,
                                fill = self.app.eyeMode.eyeColor,
                                outline = self.app.eyeMode.eyeColor)
            canvas.create_oval(cx - self.spacing/3 - radius, 
                                cy - self.spacing/4 - radius,
                                cx - self.spacing/3 + radius, 
                                cy - self.spacing/4 + radius,
                                fill = self.app.eyeMode.eyeColor,
                                outline = self.app.eyeMode.eyeColor)

            #eyes
            canvas.create_image(cx + self.spacing/3, 
                                cy - self.spacing/4,
                                image = ImageTk.PhotoImage(self.rightEye))
            canvas.create_image(cx - self.spacing/3, 
                                cy - self.spacing/4,
                                    image = ImageTk.PhotoImage(self.leftEye))
        
            #eyebrows
            eyeSpacing = self.spacing
            rightEyebrow = self.app.eyebrowMode.savedEyebrow
            leftEyebrow = self.app.eyebrowMode.getOtherEyebrow(rightEyebrow)

            scaledRightEyebrowList = [] 
            scaledLeftEyebrowList = []

            for value in rightEyebrow:
                scaled = value * self.scale * 0.5
                scaledRightEyebrowList.append(scaled)

            for value in leftEyebrow:
                scaled = value * self.scale * 0.5
                scaledLeftEyebrowList.append(scaled)

            scaledRightEyebrow = (scaledRightEyebrowList)
            scaledLeftEyebrow = (scaledLeftEyebrowList)

            eyebrowSpacing = self.app.eyebrowMode.spacing * self.scale
            x = cx + eyeSpacing/6
            y = cy - eyeSpacing/5 - eyebrowSpacing
            self.app.eyebrowMode.drawCanvasEyebrow(canvas,
                            self.app.eyebrowMode.savedEyebrowIndex, x, y)
            self.app.eyebrowMode.drawOtherEyebrow(canvas, 
                            self.app.eyebrowMode.savedEyebrowIndex, 
                            x - eyebrowSpacing, y, leftEyebrow)
            
            #nose
            canvas.create_image(cx, cy, 
                                image = ImageTk.PhotoImage(self.nose))

            #mouth
            spacing = 70 * self.scale #between nose and mouth
            mouth = self.spriteMouthList[i]
            canvas.create_image(cx, cy + spacing, 
                image = ImageTk.PhotoImage(self.scaleImage(mouth,self.scale)))

            #hair
            hairImage = self.scaleImage(self.app.hairMode.savedHair, self.scale)
            canvas.create_image(cx, cy, 
                        image = ImageTk.PhotoImage(hairImage))

        #draws strokes 
        for stroke in self.strokeList:
            for i in range(len(stroke)-1):
                canvas.create_line(stroke[i][0], stroke[i][1], 
                                   stroke[i+1][0], stroke[i+1][1],
                                   fill = self.app.exportSpriteSheetMode.color,
                                   width = 10)

#ending screen of modal app
class ExitMode(Mode):
    def keyPressed(self, event):
        if (event.key == "Left"):
            self.app.setActiveMode(self.app.exportSpriteSheetMode)
        elif (event.key == "r"):
            MyModalApp.appStarted(self.app)

    def redrawAll(self, canvas):
        restartInstructions = '''
        Thank you for using Emoji Spritesheet Maker!
        Press the 'r' key to create another sprite sheet
        '''
        canvas.create_text(self.width/2, self.height/2, 
                            text = restartInstructions,
                            font = "Arial 20 bold")

###############################################################################
# main
###############################################################################
def runModalApp():
    MyModalApp(width=1200, height=800)

def main():
    runModalApp()

if (__name__ == '__main__'):
    main()
