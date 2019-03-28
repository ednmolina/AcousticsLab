"""
This script will output the eigenmodes and frequencies expected from a
circular room.
Input parameters will be: temperature of the room, molecular weight of the gas
in the room (here it is air which is composed of 78% nitrogen, 21% oxygen,
1% argon), the fraction of air that is water,  the dimensions of the room,
and the current barometric pressure.
"""

import numpy as np
from scipy import special

" Set the temperature of the room "
T_C = 23.8
T_K = T_C + 273.15

" Calculate fraction of air that is water based on Arden Buck Equation "
# Calculate Saturation Vapor pressure
SVP = 0.61121 * np.exp((18.678 - (T_C/234.5))*((T_C)/(257.14+T_C)))  #kPa; Buck Equation

# Measured Barometric Reading in kPA and humidity of the room
P = 100.3 #kPa
h = .348

# Fraction of air that's water
X = h * (SVP/P)

" Calculate heat capcity of the wet air"
R = 8.314
Cv_H2O = 75.2
Cv =(X* Cv_H2O) + ((1-X)*((5*R)/(2)))
Cp = Cv + R
gamma = Cp/Cv

" Calculate the molecular weight of air based on atmoic masses"
# Atomic masses
N2 = 14.0067*2
H2O = 1.0079*2 + 15.9994
O2 = 15.9994 * 2
Ar = 39.948

# Molecular Weight of the Air
"Molecular Weight of the Air"
M = (H2O * X) + ((1-X)*(.78*N2 + .21*O2 + .01*Ar))

" Compute the speed of sound in that air given the parameters above "
c = np.sqrt((gamma*R*T_K)/(M/1000))

" Set the radius and height of the room "
# Units of meters
Rad = 121*10**-3
lz = 44.4 * 10**-3

" Set the modes we will explore, here the maxiumum mode will be n = 6 "
n = 6
nz = np.linspace(0, n, n+1)

" Compute the Bessel Function Values for the nodes "
BesselList = list()
for i in range(11):
    BesselList.append(special.jnp_zeros(i,n+2))

BesselList[0]=np.roll(BesselList[0], 1)
BesselList[0][0] = 0
ZerosColumn = np.zeros((11, 1))
# This is a table of bessel values
BesselList = np.append(ZerosColumn, BesselList, axis=1)

" Compute the Frequencies in the Room "
Frequencies = list()
for m in range(len(nz)):
    for n in range(len(nz)):
        for z in range(len(nz)):
            f = c/2*np.sqrt((BesselList[m][n]/(np.pi * Rad))**2+(nz[z]/lz)**2)
            Frequencies.append([m, n, z, f])
# Conver the list to a numpy array
Frequencies = np.reshape(Frequencies, (len(nz)**3, 4))

"Find the set of uniq frequecnies"
unique_freq = list()
for i in Frequencies.T[2]:
    if i not in unique_freq:
        unique_freq.append(i)

print ("Eigenmodes for the Cylindrical Room")
print ("nx  ny  nz freq")
freq_set = Frequencies.T[3]

indicies = {value : [i for i, v in enumerate(freq_set) if v == value] for value in freq_set}

for key in sorted(indicies.keys()):
    for i in range(len(indicies[key])):
        Frequencies_index = indicies[key][i]
        print (Frequencies[indicies[key][i]][0], Frequencies[indicies[key][i]][1], Frequencies[indicies[key][i]][2], round(key, 2))
    print ("\n")
