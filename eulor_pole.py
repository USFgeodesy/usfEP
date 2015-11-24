# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:12:02 2015
Euler_pole

Utilities for calculating Euler Pole



@author: rNick Voss
"""

class pole:
    '''
    attributes:
        location
        velocity
        uncertianty
        info: optional string desribing pole 
    '''
    def init(self,location,velocity,uncertainty,info = None):
        self.location = location
        self.velocity = velocity
        self.uncertianty = velocity
        self.info = info 
    
    def plot(self):
        '''
        plot the pole on a map
        '''
        
        