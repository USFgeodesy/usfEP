# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:52:32 2015

Euler_calculate

Utilites for calculating pole 

ll2geocentric : 
    - convert lat lon to geocentric coordinates

@author: Nick Voss
nvoss@mail.usf.edu
"""
import numpy as np 

def ll2geocentric(latitude,longitude):
    '''
    inputs:
        latitude: latitude of GPS station
        longitude: longitude of GPS station
    returns:
        geocentirc vector: vector describing gps position in geocentric coordinates
    '''
    Re = 6371.0 #radius of the earth in km
    rLat = np.radians(latitude)
    rLon = np.radians(longitude)
    Rx = Re*np.cos(rLat)*np.cos(rLon)
    Ry = Re*np.cos(rLat)*np.sin(rLon)
    Rz = Re*np.sin(rLat)
    return [Rx,Ry,Rz]

def ll2local(lat,lon):
    '''
    inputs:
        lat: latitude of gps
        lon: longitude of gps
    returns:
        vectors of local coordinate system
        - north
        - east
        - up
    '''
    Re = 6371.0 #radius of the earth in km
    rLat = np.radians(latitude)
    rLon = np.radians(longitude)
    n = -np.sin(rLat)*np.cos(rLon)
    e = -np.sin(rLat)*np.sin(rLon)
    u = np.cos(rLon)
    return n,e,u
    
    
def velocities(omega,R):
    '''
    calculate the velcity at a postion on the earth service
    inputs:
        omega: euler vector
        R: position vecor
    '''
    


