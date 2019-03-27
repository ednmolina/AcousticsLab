"""
This code will calculate the eigenmodes of a rectangular room based on the:
temperature of the room, molecular weight of the gas in the room (here it is
air which is composed of 78% nitrogen, 21% oxygen, 1% argon), the fraction
of air that is water, and the current barometric pressure.
"""

import numpy as np

" Set the temperature of the room "
# Convert temperature from C to absolute temperatue
T_C = 24.3
T_K = T_C + 273.15

" Calculate fraction of air that is water based on Arden Buck Equation "
# Calculate Saturation Vapor pressure
SVP = 0.61121 * np.exp((18.678 - (T_C/234.5))*((T_C)/(257.14+T_C)))  #kPa; Buck Equation

# Current Barometric Reading in kPa and humidity of the rooms
P = 100.3
h = 0.44

# Fraction of air that's Water\
X = h * (SVP/P)

" Calculate heat capcity of the wet air"
# Assuming nitrogen and oxygen can be ideal diatomic tag_hashes
R = 8.314 # Ideal Gas Constant
Cv_H2O = 75.2 # Vapor pressure of water
Cv =(X* Cv_H2O) + ((1-X)*((5*R)/(2)))
Cp = Cv + R
gamma = Cp/Cv

" Calculate the molecular weight of air based on atmoic masses"
# Atomic masses
N2 = 14.0067*2
H2O = 1.0079*2 + 15.9994
O2 = 15.9994 * 2
Ar = 39.948

# Molecular weight
M = (H2O * X) + ((1-X)*(.78*N2 + .21*O2 + .01*Ar))

" Compute the speed of sound in the air "
"Speed of Sound"
c = np.sqrt((gamma*R*T_K)/(M/1000))
print "The speed of sound is: ", c, " m/s."

" Set the n we will explore "
nx = np.linspace(0, 4, 5)
ny = np.linspace(0, 4, 5)
nz = np.linspace(0, 4, 5)

" Set the dimentions of the room "
# Dimensions are in meters
lx = 203.10 * 10**-3
ly = 161.64 * 10**-3
lz = 140.70 * 10**-3

" Calculate frequencies "
xlist = list()
data = list()
for x in range(len(nx)):
    for y in range(len(ny)):
        for z in range(len(nz)):
            f = np.sqrt((x/lx)**2+(y/ly)**2+(z/lz)**2) * (c/2)
            data.append([x, y, z, f])
data = np.reshape(data, (len(nx)*len(ny)*len(nz), 4))

" Find the set of unique frequencies-eigenmodes "
unique_freq = list()
for i in data.T[3]:
    if i not in unique_freq:
        unique_freq.append(i)

" Print out the frequencies and their associated modes, n_x, n_y, n_z "
freq_set = data.T[3]

indicies = {value : [i for i, v in enumerate(freq_set) if v == value] for value in freq_set}

print "Eigenmodes for the Rectangular Room"
print "nx  ny  nz freq"

for key in sorted(indicies.keys()):
    for i in range(len(indicies[key])):
        data_index = indicies[key][i]
        print data[indicies[key][i]][0], data[indicies[key][i]][1], data[indicies[key][i]][2], round(key, 2)
    print "\n"
