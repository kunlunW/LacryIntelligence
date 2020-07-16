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

from CellTracker.data import Data

#############################################################
#############################################################
    

class CellTrack():
    def __init__(self,cell_id, initial_time, InitialData):
        
        ##storage of data
        self.cell_id=cell_id
        self.cell_data=dict()
        self.cell_data[initial_time]=InitialData
        
        ##for tracking
        self.last_seen=max(self.cell_data.keys())
        self.missing=False
        self.finished=False
        
    def __repr__(self):
        print("Contains Data:")
        for timepoint in self.cell_data.keys():
            print(f"Time {timepoint}:\t {self.cell_data[timepoint]}")
        print(f"Last scene at time: {self.last_seen}")
        return str(f"CellTrack ID# {self.cell_id}")
     

    ###functions for tracking

    def returnID(self):
        return self.cell_id
    
    def returnPositionAtTime(self,time):
        return self.cell_data[time].returnPosition()
    
    def returnSpeedAtTime(self,time):
        try:
            t1=self.cell_data[time-1].returnPosition()
            t2=self.cell_data[time].returnPosition()
            ret= np.linalg.norm(t2-t1)
        except:
            ret= False
        return ret
        
    def returnAreaAtTime(self, time):
        return self.cell_data[time].returnArea()
    
    def returnDataAtTime(self,time):
        return self.cell_data[time]
    
    def addDataAtTime(self,time,DataObject):
        self.cell_data[time]=DataObject
        self.current_time=time
        self.last_seen=max(self.cell_data.keys())
        return
    
    def terminateTrack(self):
        self.finished=True
        self.missing=True
        
    def goMissing(self):
        self.missing=True
        
    def notMissing(self):
        self.missing=False
    
    def isMissing(self):
        if self.missing==True:
            ret=True
        else:
            ret=False
        return ret
    
    def lastSeen(self):
        return self.last_seen
    
    def isFinished(self):
        return self.finished

    
#############################################################
#############################################################

class CellTracker():
    
    def __init__(self, max_missing=25, dist_threshold=120):
        self.nextObjectID=0
        self.time=0
        self.cells=dict()
        self.max_missing = max_missing
        self.dist_threshold=dist_threshold
        
    def register(self, CellData):
        self.cells[self.nextObjectID]=CellTrack(
                                          cell_id=self.nextObjectID, 
                                          initial_time=self.time, 
                                          InitialData=CellData
                                          )
        self.nextObjectID += 1

    def update(self, list_of_data):
        print(f"Updating at time {self.time}")
        
        ##handle when nothing to track
        if len(list_of_data) == 0:
            for ident, CellTrack in self.cells.items():
                if not CellTrack.isMissing():
                    CellTrack.goMissing()
                    if self.time-CellTrack.lastSeen()>self.max_missing:
                        CellTrack.terminateTrack()
            self.time +=1
            return

		# if we are currently not tracking any cells take the input
		# cell data and register each of them
        if len(self.cells) == 0:
            for DataPoint in list_of_data:
                self.register(DataPoint)
            self.time +=1
                
		# otherwise, are are currently tracking objects so we need to
		# try to match the input centroids to existing object
		# centroids
        else:
            
            ordered_active_centroids=list()
            ordered_active_atlas=dict()
            
            i=0
            for ident,Cell in self.cells.items():
               if not Cell.isFinished():
                   ordered_active_atlas[i]=Cell
                   ordered_active_centroids.append(Cell.returnPositionAtTime(Cell.lastSeen()))
                   i+=1
    
            
            ordered_detected_centroids=list()
            ordered_detected_atlas=dict()
            j=0
            for Data in list_of_data:
                ordered_detected_centroids.append(Data.returnPosition())
                ordered_detected_atlas[j]=Data
                j+=1
            
            ##now we should have two lists that provide the old centroids and new centroids
            ##in some order. And we have an atals that connects the ORDER of the old centroids to the data
               
            ##compute pairwise distances (can be extended to be a cost function)
            N = len(ordered_active_centroids)
            M = len(ordered_detected_centroids)
            cost = np.zeros(shape=(N, M))   # Cost matrix
            for i in range(N):
                for j in range(M):
                    try:
                        cost[i][j] = np.linalg.norm(ordered_active_centroids[i]-ordered_detected_centroids[j])
                    except:
                        pass

            assignment = []
            ##prep a list of dummy assignments as -1 (since 0 is an indexx)
            for _ in range(N):
                assignment.append(-1)
            
            ##find pairs w/ minimum distance
            row_ind, col_ind = linear_sum_assignment(cost)
            
            ##assign the ith member of the active centroids to its associated match in the detected centroids
            for i in range(len(row_ind)):
                assignment[row_ind[i]] = col_ind[i]
                print(f"assigned {row_ind[i]} to {col_ind[i]}")
      
            #deal with any unassignable tracks
            unassigned_tracks = []
            for i in range(len(assignment)):
                if (assignment[i] != -1):
                # check for track assigned VERY far from where it should be
                # If distance is too far, assume detected track is not lined up correctly.
                    if (cost[i][assignment[i]] > self.dist_threshold):
                        assignment[i] = -1
                        unassigned_tracks.append(i)
                        print(f"Assigment for {i} was too far away")
                    pass
                else:
                    ## if assigment was -1 assume that the track has gone missing and set it as such
                    ordered_active_atlas[i].goMissing()
                    print(f"Assigment for {i} went missing")
            

        
            ##update data for assignable tracks:
            for i in range(len(assignment)):
                if (assignment[i] != -1):
                    ordered_active_atlas[i].addDataAtTime(self.time, ordered_detected_atlas[assignment[i]])
                    print(f"Updated cell {ordered_active_atlas[i].returnID()} with new data")
            # If tracks are not detected for long time, terminate them from tracking
            for i in range(len(assignment)):
                if (self.time-ordered_active_atlas[i].lastSeen()) > self.max_missing:
                    ordered_active_atlas[i].terminateTrack()
                    print(f"Terminated track {ordered_active_atlas[i].returnID()}")
           
            for j in range(len(ordered_detected_centroids)):
                if j not in assignment:
                    self.register(ordered_detected_atlas[j])
                    print(f"Adding unassigned object {j} to tracker.")
            self.time+=1
        return 
    