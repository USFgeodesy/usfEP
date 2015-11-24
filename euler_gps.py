# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:16:37 2015

euler_gps 
    station:
        - holds GPS information 
            -postition
            -velocity
            -uncertianty
    network:
        - continer for GPS stations 
@author: Nick Voss
"""

class station:
    '''
    Attributes:
        position
        velocitity 
        covariance
    '''
    def init(self,name,posistion,velocity,covariance)
        self.name = name        
        self.postion = posistion
        self.velocity = velocity 
        self.covariance = covariance 
    
    def map(self):
        '''
        plot station position with error ellipses
        '''

class network:
    '''
    container for GPS objects
    '''
    def init(self,name,stations):
        self.name = name
        self.stations = stations 
    
    def map(self):
        '''
        plot stations on map with error ellipses
        '''
        
        