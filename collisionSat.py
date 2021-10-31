from skyfield.api import Topos, load
from astropy import units as u
from astropy import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import sys
ts = load.timescale(builtin=True)

#This program is able to calculate the closest pass between two given satellites over the next 5 days.
#While it cannot predict collisions (yet), it can be used to verify already predicted ones.


#I used the Skyfield library's documentation to write this first part of my code. 
#See here: https://rhodesmill.org/skyfield/earth-satellites.html


#Load all satellite Two-Line Element sets from the given file(s)
#I used the satellite data provided by the celestrak.com website, since it is vast, accurate and easily accessible.
sat_url = 'https://celestrak.com/NORAD/elements/active.txt'
tle_satellites = load.tle_file(sat_url, reload = True)
print("Loaded", len(tle_satellites), "satellites")

def calculate():

#	Search the file(s) and display names and epochs of the desired satellites
	NORAD_ID1 = input("\nPlease enter the NORAD ID of the first desired object: ")
	NORAD_ID2 = input("\nPlease enter the NORAD ID of the second desired object: ")
	
	by_number = {sat.model.satnum: sat for sat in tle_satellites}
	satellite1 = by_number[int(NORAD_ID1)]
	satellite2 = by_number[int(NORAD_ID2)]
	print("\n", satellite1)
	print("\n", satellite2)
	print("\nCurrent epoch of sat1: ", satellite1.epoch.utc_jpl())
	print("\nCurrent epoch of sat2: ", satellite2.epoch.utc_jpl())
	
#	Compute the positions of both satellites every 0.864 seconds (0.00001 days) for the next 5 days using the SGP4 perturbation model.
	tcompute = ts.tt_jd(np.arange(satellite1.epoch.tt, satellite1.epoch.tt + 5.0, 0.00001))


#	From hereon, I did not reference the documentation and everything is my original code.


#	Initialize the necessary arrays for the calculations. 
	distancearray = []
	timearray = []
	closepassdistance = []
	closepasstime = []

	print("setup complete")

#	Compute the distance between the satellites from the tcompute array for each element, by subtracting the vectors of their current positions.
#	Enter the distance into distancearray and the time into timearray.
	for x in tcompute:
		y = (satellite2.at(x) - satellite1.at(x)).distance().km
		distancearray.append(y)
		timearray.append(x)
		print(x)

	print("done x in tcompute")

#	Initialize two more arrays, that contain the first and second derivatives of the distance between the satellites.
#	This is necessary to determine the minimum distance between them during the next 5 days.
	derivativearray = np.gradient(distancearray)
	secondderivativearray = np.gradient(derivativearray)

	print("done derivative")

#	This for-loop finds all relative minima using single-variable calculus, appending them to another array.
#	The loop first finds all instances where the derivative crosses 0. 
#	Note that I use the intermediate value theorem to do this, since the tcompute array only has datapoints every 0.864s.
#	Then, the for loop finds which of these points have a second derivative greater than 0, i.e. they are relative minima.
	i = 0
	for z in derivativearray:
		if z < 1.5 and z > -1.5:
			if secondderivativearray[i] > 0:
				j = distancearray[i]
				k = timearray[i]
				closepassdistance.append(j)
				closepasstime.append(k)
		
		i += 1

	print("\n -----------------------------")
	print("\n")
	for e in closepasstime:
		print(e)

#	Find the distance and time of the closest pass between the two satellites.
	cpd = closepassdistance.index(min(closepassdistance))
	cpt = closepasstime[cpd]

#	Print out the distance and time of the closest pass.
	print("\n", cpt.utc_datetime())
	print("\n", cpd)

#	Graph out a distance vs. time graph of the closest pass
	tgraph = ts.tt_jd(np.arange(cpt.tt - 0.001, cpt.tt + 0.001, 0.00001))
	g1 = satellite1.at(tgraph)
	g2 = satellite2.at(tgraph)

	fig, ax = plt.subplots()

	a = tgraph.utc_datetime()
	b = (g2 - g1).distance().km
	ax.plot(a, b)

	ax.grid(which='both')
	ax.set(title='Closest pass/collision between the satellites', xlabel = 'UTC')

	fig.savefig('sat-separation.png', bbox_inches='tight')

	fig.show()


#Simple loop to restart the program if desired
quit = 'r'
if quit == 'q':
	sys.exit()
elif quit == 'r':
	calculate()
	quit = input("Type 'q' to quit, or 'r' to restart: ")
