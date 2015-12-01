# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:52:32 2015

Euler_calculate

Utilites for calculating pole 

ll2geocentric : 
    - convert lat lon to geocentric coordinates

ll2local:
    -convert lon to local coordinate system 

@author: Nick Voss
nvoss@mail.usf.edu
"""
import numpy as np 

def ll2geocentric(longitude,latitude):
    '''
    inputs:
        latitude: latitude of GPS station
        longitude: longitude of GPS station
    returns:
        geocentric vector: vector describing gps position in geocentric coordinates
    '''
    Re = 6371.0 #radius of the earth in km
    rLat = np.radians(latitude)
    rLon = np.radians(longitude)
    Rx = Re*np.cos(rLat)*np.cos(rLon)
    Ry = Re*np.cos(rLat)*np.sin(rLon)
    Rz = Re*np.sin(rLat)
    return [Rx,Ry,Rz]

def ll2local(lon,lat):
    '''
    Compute the local coordinate vectors 
    inputs:
        lat: latitude of gps
        lon: longitude of gps
    returns:
        vectors of local coordinate system
        - north
        - east
        - up
    '''
    rLat = np.radians(lat)
    rLon = np.radians(lon)
    n = [-np.sin(rLat)*np.cos(rLon),-np.sin(rLat)*np.sin(rLon),np.cos(rLat)]
    e = [-np.sin(rLon),np.cos(rLon),0.0]
    u = [np.cos(rLat)*np.cos(rLon),np.cos(rLat)*np.sin(rLon),np.sin(rLat)]
    return [e,n,u]
    
    
def vPole2local(V,n,e,u):
    '''
    calculate the velocity at a postion on the earth service
    inputs:
        V: euler vector
        n: north vector for local coordinate system
        e: east vector for local coordinate system 
        u: up vector for local coordinate system 
    '''
    Vn = np.dot(V,n)
    Ve = np.dot(V,e)
    Vu = np.dot(V,u)
    if np.allclose(Vu,0.0)!=True:
        print 'Warning Vu should be 0, can not move off of sphere! Vu :',Vu
    return Vn,Ve,Vu

def euler2sphere(lon,lat,mag):
    '''
    compute the euler vector components in spherical coordinates
    '''
    omegaX = mag*np.cos(np.radians(lat))*np.cos(np.radians(lon))
    omegaY= mag*np.cos(np.radians(lat))*np.sin(np.radians(lon))
    omegaZ = mag*np.sin(np.radians(lat))
    return [omegaX,omegaY,omegaZ]

def geocentricUnitVector(latitude,longitude):
    X = np.cos(np.radians(latitude))*np.cos\
        (np.radians(longitude))
    Y = np.cos(np.radians(latitude))*np.sin\
        (np.radians(longitude))
    Z = np.sin(np.radians(latitude))
    return(X,Y,Z)   

def sphere2latlon(X,Y,Z):
    '''
    inputs:
        X : omegaX
        Y : omegaY
        Z : omegaZ
    return lon,lat,magnitude (in degrees/Myr)
    '''
    latitude = np.degrees(np.arctan2(Z,np.sqrt(X**2 + Y**2)))

    longitude = np.degrees(np.arctan2(Y,X))
    #if X < 0.0 :
        #longitude = -180.0 + longitude 
    if longitude < 0.0:
        longitude = 360+longitude
    angularVelocity = np.degrees(np.sqrt(X**2 + Y**2 + Z**2))
    return longitude,latitude,angularVelocity

    