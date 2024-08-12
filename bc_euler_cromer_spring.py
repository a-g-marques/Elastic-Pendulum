import scipy.constants as const
import numpy as np
import math
import copy
from matplotlib import pyplot as plt
from ba_Spring_Class import Spring




bob = Spring(
            name='bob',
            mass=1.5,
            k=20,
            length=1.5,
            position=np.array([1, 0], dtype=float),
            velocity=np.array([0, 0], dtype=float),
            acceleration=np.array([0, 0], dtype=float)
)


# calculatins the different energies
INITIAL_ENERGY = bob.E_T()
print("Initial E_k = ", bob.E_k())
print("Initial E_gp = ", bob.E_gp())
print("Initial E_ep = " ,bob.E_ep())
print("Initial E_T = ", INITIAL_ENERGY)
print("######################")



bob_positions = [] # storing the different locations of the mass. the values will be as a list in a list, i.e.,
                   # bob_positions[0] will be a list with 2 values, the first (bob_positions[0][0]) being the radius, and the second (bob_positions[0][1]) being the radius

CALCULATIONS = 6570 # number of calculations that will be made
DT = 0.001 # time-step of each calculation


for i in range(CALCULATIONS): # making the calculations of where the mass will be next and adding it to the list with it's positions
    bob.update_acceleration()
    bob.euler_cromer(DT)
    #if i % 25 == 0: #here, when the previous stuff isn't #'ed, i would not store every values that's calculated, although they would still be considered to make the next calculation
    bob_positions.append(copy.deepcopy(bob.position))


# calculatins the different energies
FINAL_ENERGY = bob.E_T()
print("Final E_k = ", bob.E_k())
print("Final E_gp = ", bob.E_gp())
print("Final E_ep = ", bob.E_ep())
print("Final E_T = ", FINAL_ENERGY)
print("Ratio = ", 100*(FINAL_ENERGY - INITIAL_ENERGY) / INITIAL_ENERGY, "%") # this is by how much the total enegy changed, which changes because the calculations are not exat
                                                                             # we can test the code by looking at this value, where if it's samll enough we can assume that enegy is conserved



bob_x=[] # storing the x values
bob_y=[] # storing the y values

for i in bob_positions:
        bob_x.append(i[0]*math.sin(i[1]))
        bob_y.append(i[0]*math.cos(i[1]))




bob_t=[] # storing the time values

for i in range(len(bob_x)):
    bob_t.append(DT * i)




bob_r=[] # storing the radius values
bob_theta=[] # storing the angle values

for i in bob_positions:
    bob_r.append(i[0])
    bob_theta.append(i[1])








# making a gradient of colours until line 80 for easier data visualisation
def from_hex_to_rgb(colour_in_hex):
    # passing hexdecimal colours to the same rgb colour, allowing us to make calculations with them
    return [int(colour_in_hex[i:i+2], 16) for i in range(1,6,2)]

def gradient_of_colours(initial_colour_in_hex, final_colour_in_hex, divisions):
    # splitting 2 colours (initial_colour and final_colour) into "divisions" colours, i.e., many colours in between
    initial_colour_in_rgb = np.array(from_hex_to_rgb(initial_colour_in_hex))/255
    final_colour_in_rgb = np.array(from_hex_to_rgb(final_colour_in_hex))/255
    mix_pcts = [i/(divisions-1) for i in range(divisions)]
    rgb_colours = [((1-mix)*initial_colour_in_rgb + (mix*final_colour_in_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(value*255)), "02x") for value in item]) for item in rgb_colours]



initial_colour = "#5a82c2" #blue
final_colour = "#d53535" #red


# plotting the values
ax = plt.axes()
ax.scatter(bob_t, bob_y, c=gradient_of_colours(initial_colour, final_colour, CALCULATIONS))
ax.set_xlabel('t [s]')
ax.set_ylabel('y [m]')
ax.set_title('t vs. y plot of a Vertical Spring using Euler-Cromer')
'''plt.xlim(-10, 110)
plt.ylim(-15, -5)'''
plt.show()






