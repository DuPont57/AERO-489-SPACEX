import numpy as np
from math import *

# Provided parameters
C_L_max = 1
C_L_max_TO = 1
C_L_max_L = 1

AR = 1
S = 1
b = 1

sweep_angle = 1
taper_ratio = 1
root_chord = 1
tip_chord = 1

flap_chord_ratio = 1
flap_extension_TO = 1
flap_extension_L = 1

# Calculations

# Additional lift requirements for takeoff and landing
Additional_C_L_Max_TO = 1.05 * (C_L_max_TO - C_L_max)
Additional_C_L_Max_L = 1.05 * (C_L_max_L - C_L_max)

# Max additional lift needed from flaps when extended
n_o = 1
n_i = 1
Swf_S = (n_o - n_i) * (2 - (1 - taper_ratio) * (n_i + n_o)) / (1 + taper_ratio)

K_A = (1 - 0.08 * pow(cos(sweep_angle), 2)) * pow(cos(sweep_angle), 0.75)
del_c_l_max = max(Additional_C_L_Max_TO, Additional_C_L_Max_L) * Swf_S * K_A

# Calculate additional lift obtained from flaps when extended
C_L_delta_f = 1
flap_extension = 1
K_prime = 1

# Plain flaps
C_l_flaps_extended_plain = C_L_delta_f * flap_extension * K_prime


