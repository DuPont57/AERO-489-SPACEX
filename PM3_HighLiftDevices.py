import numpy as np
from math import *

# Provided parameters

# Roskam Table 3.1
C_L_max = 1.6
C_L_max_TO = 2.0
C_L_max_L = 2.5

AR = 9.45 # Boeing 737
S = 2643.29 # sq ft - taken from PM 1
b = sqrt(AR * S) # ft

# Parameters for the Boeing 737
sweep_angle = radians(25)
taper_ratio = 0.159
root_chord = 25.3 # ft
tip_chord = 5.8 # ft

flap_chord_ratio = 0.3
flap_extension_TO = radians(35)
flap_extension_L = radians(40)

# Calculations

# Additional lift requirements for takeoff and landing
Additional_C_L_Max_TO = 1.05 * (C_L_max_TO - C_L_max)
Additional_C_L_Max_L = 1.05 * (C_L_max_L - C_L_max)

# Max additional lift needed from flaps when extended
n_o = 1
n_i = 1
Swf_S_TO = 0

K_A = (1 - 0.08 * pow(cos(sweep_angle), 2)) * pow(cos(sweep_angle), 0.75)
del_c_l_max = max(Additional_C_L_Max_TO, Additional_C_L_Max_L) * Swf_S * K_A

# Calculate additional lift obtained from flaps when extended

# Fowler Flaps
del_C_l_TO_fowler = 2 * pi * 0.47 * flap_extension_TO
del_C_l_L_fowler = 2 * pi * 0.4 * flap_extension_L

# Calculate max additional lift obtained from flaps when extended
C_l_max_TO_fowler = 0.85 * del_C_l_TO_fowler
C_l_max_L_fowler = 0.85 * del_C_l_L_fowler


