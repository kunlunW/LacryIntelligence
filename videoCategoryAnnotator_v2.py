# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:33:59 2020

@author: scoyl
"""

###############################################################################
####[SETUP/INITIALIZE]#########################################################
###############################################################################


############################################
### IMPORT HELPER PACKAGES              ####
############################################

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from os import path
import re
import cv2

############################################



############################################
### setup some global params             ###
############################################

# rescale videos by this
scale = 1         

# radius of the box for an image
boxRad = 50        

############################################



###########################################
## TO USE:: PUT FILES IN 'movies' dir    ##
## Creates a list of openCV captures     ##
###########################################

moviesList=list()
for movie in os.listdir("movies"):
    moviesList.append("movies/"+movie)
    
###########################################
    


###########################################
##   Create CaptureList                ####
###########################################

capList=list()
for movie in moviesList:
    capList.append(cv2.VideoCapture(movie))
    
###########################################
    
    

###########################################
##   Create Main Window                ####
###########################################        

mainWindowName="image"              
cv2.namedWindow(mainWindowName)

###########################################
         


###########################################
## Create categoriesList            #######
###########################################

categoriesList=list(["active", "dormant"])

for cat in categoriesList:
    if not(path.exists(cat)):
        os.mkdir(cat)
        
###########################################





###############################################################################
######[   CLASSES    ]#########################################################
###############################################################################
        
############################################
### CoordinateStore class:              ####
############################################
###                                     ####
### Temporary hold and display of       ####
### coordinates associated with a frame ####
###                                     ####        
############################################

class CoordinateStore:
    def __init__(self,window=mainWindowName,boxRad=50):
        self.points = []
        self.status='off'
        self.window=window
        self.framesList=list()
        self.frame='None'
        self.boxRad=boxRad
        self.refPoint=(0,0)
        
    def select_point(self,event,x,y,flags,param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.status=='on':
                if flags==(cv2.EVENT_FLAG_SHIFTKEY):
                    self.playFrameslist()
                else:
                    self.refPoint = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            if self.status=='on':
                if flags==(cv2.EVENT_FLAG_SHIFTKEY):
                    self.playFrameslist()
                else:
                    a=(0<(x+self.boxRad)<self.frame.shape[1])
                    b=(0<(x-self.boxRad)<self.frame.shape[1])
                    c=(0<(y-self.boxRad)<self.frame.shape[0])
                    d=(0<(y+self.boxRad)<self.frame.shape[0])
            
                    if a and b and c and d:
                        p1=(x-self.boxRad,y-self.boxRad)
                        p2=(x+self.boxRad,y+self.boxRad)
                        cv2.rectangle(self.frame, p1, p2, (255,0,0), 2, 1)
                        cv2.imshow(self.window,self.frame)
                        self.points.append((x-self.boxRad,y-self.boxRad,self.boxRad*2,self.boxRad*2))
                        print((x,y))
                        
        
        
        # if event == cv2.EVENT_LBUTTONDBLCLK:
        #     if self.status=='on':
        #         a=(0<(x+boxRad)<self.frame.shape[1])
        #         b=(0<(x-boxRad)<self.frame.shape[1])
        #         c=(0<(y-boxRad)<self.frame.shape[0])
        #         d=(0<(y+boxRad)<self.frame.shape[0])
        
        #         if a and b and c and d:
        #             p1=(x-boxRad,y-boxRad)
        #             p2=(x+boxRad,y+boxRad)
        #             cv2.rectangle(self.frame, p1, p2, (255,0,0), 2, 1)
        #             cv2.imshow(self.window,self.frame)
        #             self.points.append((x-self.boxRad,y-self.boxRad,self.boxRad*2,self.boxRad*2))
        #             print((x,y))

    
    def playFrameslist(self):
        for i in range(len(self.framesList)):
            cv2.imshow(self.window,self.framesList[i])
            cv2.waitKey(15)
        cv2.imshow(self.window, self.frame)
        cv2.waitKey(15)
    
    def resetFrameslist(self):
        self.framesList=list()
        
    def addFrame(self,frame):
        self.framesList.append(frame)
        self.frame=frame
    
    def setFrame(self,frame):
        self.frame=frame
        
    def reset(self):
        self.points=[]

    def turnOff(self):
        self.status='off'
    
    def turnOn(self):
        self.status='on'

        
   
############################################
### insantiate coordinatestore class &  ####
### connect it to the openCV GUI        ####
############################################
        
myCoordinateStore = CoordinateStore(boxRad=boxRad)
cv2.setMouseCallback(mainWindowName,myCoordinateStore.select_point)

############################################        
        
        



###############################################################################
####[FUNCTIONS]################################################################
##############################################################################

                        
############################################
### randomCapture function:             ####
############################################
###                                     ####
### Selects a random video from capList ####
### and picks a frame at random from it ####
###                                     ####
### shows buffer no. of frames before   ####q
### serving up the final frame.         ####
###                                     ####
### if Q is pressed will ret False      ####
###                                     ####  
### returns Bool (for exit),  frame     ####
###                                     ####
############################################
                 
def randomCapture(capList, window, coordStore,buffer=60):
    coordStore.resetFrameslist()
    randIndex= np.random.randint(len(capList))        
    randFrame= np.random.randint(int(capList[randIndex].get(cv2.CAP_PROP_FRAME_COUNT)))
        
    capList[randIndex].set(1,randFrame)
    for i in range(buffer):
        ok, frame = capList[randIndex].read()
        coordStore.addFrame(frame)
        cv2.imshow(mainWindowName,frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
           return False,frame
    return True,frame, randIndex, randFrame
    
############################################        
############################################





############################################
### clickCategory function:             ####
############################################
###                                     ####
### Will process the clicking for       ####
### 'category' given a frame, window,   ####
### and coordinate storage object       ####
###                                     ####    
###  if (S) is pressed:                 ####      
### Crops and saves all images in the   ####
### coordStore list and writes them to  ####
### the category directory              ####
###                                     #### 
###                                     ####
### if (X) ret True; (Q) ret False      ####
### returns Bool (for exit)             ####
###                                     ####
############################################


def clickCategory(category,frame,window,coordStore):
    
    #make a scratch frame and a backup frame
    scratchFrame=frame.copy()
    originalFrame=frame.copy()
    
    #reset and activate the coordinate store
    coordStore.reset()
    coordStore.turnOn()
    coordStore.setFrame(scratchFrame)

    cv2.putText(scratchFrame, "Select "+category+": (S)ave (X)cancel (Q)uit                    Shift-click to replay", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)            
    cv2.imshow('image', scratchFrame) # show frame on window
    key = cv2.waitKey(0) & 0xFF
    
    if key == ord('s'):
        for (x,y,w,h) in coordStore.points:
            cropped = originalFrame[y:y+w , x:x+h] # both opencv and numpy are "row-major", so y goes first
            cv2.imwrite(category+"/"+str(len(os.listdir(category))+1)+".png",cropped)
        
    elif key == ord("x"):
        print("skipping")
        
    elif key == ord("q"):
        return False
    
    return True

############################################
############################################
    





############################################
### cleanExit function:                 ####
############################################
###                                     ####
### releases all capture objects in     ####
### capList, destroys the GUI, and      ####
### triggers an exit                    ####
###                                     ####
############################################
 
def cleanExit(capList):
    for cap in capList:
        cap.release()
    cv2.destroyAllWindows()
    sys.exit()
    return

############################################
############################################
    
    





###############################################################################
####[   MAIN LOOP   ]##########################################################                                      
###############################################################################


while(True):
    ok,randomFrame,idx,fr=randomCapture(capList, window=mainWindowName,coordStore=myCoordinateStore, buffer=60)
    if not ok:
        cleanExit(capList)
    for cat in categoriesList:
        ok=clickCategory(cat,randomFrame,mainWindowName,myCoordinateStore)
        if not ok:
            cleanExit(capList)
            
            
###############################################################################


