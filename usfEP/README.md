# usfEP
Inversion of GPS data for Euler Poles 

Any motion of on the surface of a sphere can be described by a 
rotation about a axis. This axis is the euler pole. 


and d = V = column vector of GPS data 

V = omega .(R x m)  

omega is the Euler Pole 

R is the vector pointing towards the GPS location from center of the earth
Rz = Re*cos(Lat)*cos(Lon)
Ry = Re*cos(Lat)*sin(Lon)
Rz =Re*sin(Lat)
m is the velocity 


Inversion is doing Weighted Least Squares using pjInvert
	-outputs solution,covariance, and resolution matrices

Components:
	euler_gps: class for holding gps data
	eulr_pole: class for hodling euler pole
	euler_calculate: utilities for calculing euler pole
	euler_plot: plotting routines
	
	

