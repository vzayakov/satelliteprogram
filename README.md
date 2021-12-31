I created this program in order to calculate potential satellite collisions. 
While it cannot predict collisions (yet), it can be used to verify the collisions that NORAD predicts. 
It uses an implementation of the SGP4 perturbation model from a Python library called Skyfield, in order to compute the satellites' locations up to 5 days in the future.

Required Dependencies: Skyfield API; Astropy; matplotlib; numpy

How to Use:

Clone the repository or just download the collisionSat.py file to your computer.
Run the program in the Shell or Terminal.
Pick the NORAD IDs of the two satellites you want to investigate. Input them when the program asks you to do so.
Wait. It will take the program a couple of minutes to complete its calculations.
Observe its outputs. There will be a date and distance of the closest pass in the Shell/Terminal, and also a graph of the two minute window around the closest pass.
Quit, or restart the program.

By Victor Zayakov
