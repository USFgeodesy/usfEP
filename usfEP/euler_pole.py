# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 21:12:02 2015
Euler_pole

Utilities for calculating Euler Pole



@author: rNick Voss
"""
import matplotlib.pylab as plt
from mpl_toolkits.basemap import Basemap

class pole:
    '''
    attributes:
        location
        velocity
        angular velocity components
        model  ' modeled velocities'
        uncertianty
        info: optional string desribing pole 
    '''
    def __init__(self,location,velocity,angularvelocity,model,uncertainty = None,info = None):
        self.location = location
        self.velocity = velocity
        self.ang_vel = angularvelocity
        self.uncertianty = uncertainty
        self.info = info 
        self.model = model
    
    def plot(self):
        '''
        plot the pole on a map
        '''
        # set up orthographic map projection with
        # perspective of satellite looking down at 50N, 100W.
        # use low resolution coastlines.
        map = Basemap(projection='ortho',lat_0=self.location[1],lon_0=self.location[0],resolution='l')
        # draw coastlines, country boundaries, fill continents.
        map.drawcoastlines(linewidth=0.25)
        map.drawcountries(linewidth=0.25)
        map.fillcontinents(color='coral',lake_color='aqua')
        # draw the edge of the map projection region (the projection limb)
        map.drawmapboundary(fill_color='aqua')
        # draw lat/lon grid lines every 30 degrees
        map.scatter(self.location[0],self.location[1],latlon = True,marker = '*',s = 20)
        plt.show()