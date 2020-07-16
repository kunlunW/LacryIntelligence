# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:31:35 2020

@author: scoyl
"""

import numpy as np
import cv2
from scipy.optimize import linear_sum_assignment
import os
import re

#############################################################
#############################################################

class Data():
    def __init__(self, position, area,contour):
        self.position=position
        self.area=area
        self.contour=contour
        
    def __str__(self):
        my_string=str(f"Position: {self.position}\t Area: {self.area}")
        return my_string
        
    def returnPosition(self):
        return self.position
    
    def returnContour(self):
        return self.contour
    
    def returnArea(self):
        return self.area
    
#############################################################
#############################################################
    
