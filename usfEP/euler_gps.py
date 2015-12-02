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
from euler_calculate import * 
from euler_pole import pole 
from pjInvert import * 
import numpy as np 
import pandas as pd 
import copy 
from mpl_toolkits.basemap import Basemap
import itertools

class station:
    '''
    Attributes:
        position
        velocitity 
        covariance
    '''
    def __init__(self,name,position,velocity,covariance):
        self.name = name        
        self.position = position
        self.velocity = velocity #[east,north,up]
        self.covariance = covariance 
    
    def map(self):
        '''
        plot station position with error ellipses
        '''

class network:
    '''
    container for GPS objects
    
    also contains Observation and G matrix for inversion
    
    methods:
        plotmap : plot stations on a map with velociy vectors
        genG : generate greens function matrix
        invert: invert network for Euler pole 
    '''
    def __init__(self,name,stations):
        self.name = name
        self.stations = stations 
        self.Obs = None
        self.G = None
        self.modeled = None
    
    def plotmap(self):
        '''
        plot stations on map with error ellipses
        '''        '''
        plot the pole on a map
        '''
        #get center of stations
        lons,lats,x,y, = [],[],[],[]
        for sta in self.stations:
            if sta.position[0]<0.0:
                lons.append(sta.position[0]+360.0)
            else:
                lons.append(sta.position[0])
            lats.append(sta.position[1])
            x.append(sta.velocity[0])
            y.append(sta.velocity[1])
        meanLat = np.mean(lats)
        meanLon = np.mean(lons)
        # set up orthographic map projection 
        # use low resolution coastlines.
        
        map = Basemap(projection='ortho',lat_0=meanLat,lon_0=meanLon,resolution='l')
        # draw coastlines, country boundaries, fill continents.
        map.drawcoastlines(linewidth=0.25)
        map.drawcountries(linewidth=0.25)
        map.fillcontinents(color='coral',lake_color='aqua')
        # draw the edge of the map projection region (the projection limb)
        map.drawmapboundary(fill_color='aqua')
        # draw lat/lon grid lines every 30 degrees
        map.quiver(lons,lats,x,y,angles='uv', scale_units='xy', scale=1E-4,latlon = True,color = 'k')
        #if self.modeled != None:
            #map.quiver(lons,lats,self.modeled[0:len(self.stations)-1],self.modeled[len(self.stations):-1],angles='uv', scale_units='xy', scale=1E-4,latlon = True,color = 'r')
        plt.show()
        
    def genG(self):
        '''
        generate G matrix for inversion problem using station in network
        '''
        #initialize empty G
        G = np.zeros((len(self.stations)*2,3))
        for i,station in enumerate(self.stations):
            #get R
            R = ll2geocentric(station.position[0],station.position[1])
            #get e,n,u
            lc = ll2local(station.position[0],station.position[1])
            #get gross R and enu
            G[i,0] = np.cross(R,lc[0])[0] #e 
            G[i,1] = np.cross(R,lc[0])[1] #e
            G[i,2] = np.cross(R,lc[0])[2] #e
            G[i+len(self.stations)][0] = np.cross(R,lc[1])[0] #n 
            G[i+len(self.stations)][1] = np.cross(R,lc[1])[1] #n
            G[i+len(self.stations)][2] = np.cross(R,lc[1])[2] #n            
        return G 
        
    def invert(self):
        # set up observation vector
        V = np.zeros(len(self.stations)*2)
        for i,station in enumerate(self.stations):
            V[i] = station.velocity[0]
            V[i+len(self.stations)] = station.velocity[1]
        # need it as pandas series for pjInvert
        #set up index array
        ind = []
        for i in range(len(V)):
            if i < len(self.stations):
                ind.append('East ' + self.stations[i].name)
            else:
                ind.append('North ' + self.stations[i-len(self.stations)].name)
        S = pd.Series(V,index = ind)
        # set up a weight array
        covariance = []
        for i in range(len(V)):
            if i < len(self.stations)-1:
                covariance.append(self.stations[i].covariance[0])
            else:
                covariance.append(self.stations[i-len(self.stations)].covariance[1])
        w = pd.Series(covariance,index = ind)
        #add weights inversely proportional to the covariance
        Obs = data(S,(1.0/w))
        # set up Greens function matrix as pjInvert G object 
        G = self.genG()
        gFrame = pd.DataFrame(G,index = ind, columns = ['X','Y','Z'])
        grns_fnc = greenfnc('Euler Pole',gFrame)
        # add greens function and observations to network object
        self.Obs = Obs
        self.G = grns_fnc
        angV = invert_methods.weightedLeastSquares(grns_fnc,Obs)
        #extract components of angular velocity
        X = angV[0]
        Y = angV[1]
        Z = angV[2]
        #compute the modeled displacements
        model = np.dot(G,[X,Y,Z])
        #calculate the residual 
        residual = V-model
        longitude,latitude,angularVelocity = sphere2latlon(X,Y,Z)
        print 'Lat,Lon,AngV (deg/Myr) :',latitude,longitude,angularVelocity 
        ePole = pole([longitude,latitude],angularVelocity,angV,model)
        print 'AVE Residual :', np.mean(np.abs(residual))
        #add modeled displacements to network object 
        self.modeled = model
        return ePole
    def jackknife(self):
        '''
        use the jacknife method to calculate station importance
        and pole inversion stability
        
        removes each station one at a time and reinvert
        '''
        return
        
        
    def jackknife(self):
        '''
        preform jackknife test for pole unvertianty 
        go through all netwrok comonations and reinverting
        
        returns list of poles
        '''
        polesList = []
        for i in range(2,len(self.stations)):
            t = list(set(itertools.combinations(self.stations,i)))
            for combo in t:
                net2 = copy.deepcopy(self)
                net2.stations = combo
                polesList.append(net2.invert())    
        return polesList
        
def txt2network(fname,name):
    '''
    read in a text file with the station names and info 
    #Stn      Lon          Lat    Ve(mm/yr) Vn(mm/yr) Vu(mm/yr) SigVe(mm/yr)\\ 
    SigVn(mm/yr) SigVu(mm/yr)
    '''
    data  = pd.read_csv(fname,delim_whitespace = True)
    stations = []
    for i,sta in enumerate(data.Sta):
        stations.append(station(sta,[data.Lon.values[i],data.Lat.values[i]],\
        [data.Ve.values[i],data.Vn.values[i],data.Vu.values[i]],[data.SigVe.values[i],data.SigVn.values[i],data.SigVn.values[i]]))
    net = network(name,stations)
    return net 
