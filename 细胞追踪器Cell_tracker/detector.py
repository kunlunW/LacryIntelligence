# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:32:17 2020

@author: scoyl
"""
import numpy as np
import cv2
from scipy.optimize import linear_sum_assignment
import os
import re

from CellTracker.data import Data


class Detector():
    def __init__(self, min_area=100, max_area=25000):
        self.min_area=min_area
        self.max_area=max_area
    
    def detect(self, cellpose_mask_image):
        obs_found=np.max(cellpose_mask_image)
        objects_list=list()
        for i in range(obs_found):
            j=i+1
            j_image=cellpose_mask_image*(cellpose_mask_image==j)
            im2, contours, hierarchy = cv2.findContours(j_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                M = cv2.moments(c)
                try:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    a=cv2.contourArea(c)
                    if a>self.min_area:
                        objects_list.append(Data(position=np.array([cX,cY]), area=a, contour=c))
                except:
                    pass
        return objects_list