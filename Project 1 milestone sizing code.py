import numpy as np
import matplotlib.pyplot as plt


### we need gross takeoff, empty and feul weight

#start with crew/pax, payload weight (given):
crew_mem = 410
mem_weight = 200 #lbs

w_crew = crew_mem * mem_weight #lbs

num_ppl = 400 #do crew bags count?

w_baggage = 30 * num_ppl  #lbs

#next split up mission into phases, focus on cruis/loiter. other phases have tables with feul fractions

cruise_range = 3500 + 200 #nm 
loiter_endurnace = 0.5 #hrs
reserve_per = 5 #%

#values from table in notes
#cruise
LD_c = 15
cj_c = 0.5

#assuming cruisng altitude of 35000 ft, mach 0.8, typical of this class of jets
M_c = 0.85
T_c = -65.61 + 459.67 #R
a_c = np.sqrt(1.4*1716*T_c)
V_c = M_c*a_c/6076.12*3600 #nm/hr
#loiter
LD_l = 18
cj_l = 0.4
#from range eq in notes, using jet eq, accounts for unit conversions
FF_cruise = np.exp(-cruise_range*cj_c/V_c/LD_c)
#from endurance eq in notes, using jet eq, accounts for unit conversions
FF_loiter = np.exp(-loiter_endurnace*cj_l/LD_l)
#non-cruise/loiter feul fractions are from table in notes, using transport jet
w_endW0 = 0.99*0.99*0.995*0.98*FF_cruise*FF_loiter*.99*.992



#5% feul reserves + trapped oil is negligible
WfW0 = (1 - w_endW0) * (1+reserve_per/100)

#this function gives the empty wieght fraction based on the function from roskam (basing off transoport jets)
def empty_weight(W_0):
    
    #A, B for regression line from transport jets
    A, B = 0.0833, 1.0383

    W_e = 10**((np.log10(W_0)-A)/B)
    WeW0 = W_e/W_0

    WeW0 = 1.02*W_0**-0.06

    return WeW0

#first guess for W_0
W_0_guess = 70000 #lbs
err = 1
#loop to find W_0
while err > 1e-3 or W_0 < 0:

    WeW0 = empty_weight(W_0_guess)
    
    W_0 = (w_crew + w_baggage)/(1-WfW0-WeW0)
    err = abs(W_0 - W_0_guess)
    W_0_guess = W_0

#getting empty weight from the estimated takeoff weight
W_e = WeW0 * W_0
W_f = WfW0 * W_0


print("Estimated Values:")
print(f"Gross Takeoff Weight W_0 = {W_0:.2f} lbs")
print(f"Empty Weight W_E = {W_e:.2f} lbs")
print(f"Fuel Weight W_F = {W_f:.2f} lbs")

#Part 8: Calculating W/S and T/W

#Flight Parameters
SFL = 9000 #ft
STOFL = 9000
rho = 0.002377 #slug/ft^3
C_L_Max_L = 2.6 #In range for transport jets for Transport Jets from roskam
a = -2.5229 #all letter values from roskam 3.4 and 3.5
b = 1.0000
c = 0.0199
d = 0.7531
sigma = 1 #taking off at sea level so density ratio = 1
CL_Max_T0 = 2
TOP25 = STOFL/37.5

#Calculating using roskam equations for landing constraint
V_Stall_L = np.sqrt(SFL/0.507) * 1.688
Wing_Loading_L = 0.5 * rho * V_Stall_L **2 * C_L_Max_L
Total_Weight_Ratio = (W_0-W_f)/W_0

#finding the max wing loading for our landing length
Wing_Loading_TO = Wing_Loading_L / Total_Weight_Ratio 


#creating graph for takeoff constraints
def TW(WS):
    return WS / (sigma * CL_Max_T0 * TOP25)

def W_S(W_S,T_W):
    return np.ones_like(T_W) * W_S

#plotting the constraint graph and shading in feasible region
plot_WS = np.linspace(0,1.1 * Wing_Loading_TO,100)
plot_TW = np.linspace(0,1,100)

WS = 150
TW_Ratio = 0.35

plt.plot(W_S(Wing_Loading_TO,plot_TW),plot_TW,label = "Landing Constraint")
plt.plot(plot_WS,TW(plot_WS),label = "Takeoff Constraint")
plt.plot(WS,TW_Ratio,"ro",label =  "Selected Values")
plt.fill_between(np.linspace(0,Wing_Loading_TO,100),TW(np.linspace(0,Wing_Loading_TO,100)),1.0,color = "green",alpha = 0.25,label="Feasible Region")
plt.xlabel("Take off Wing Loading (psf)")
plt.ylabel("Takeoff Thrust to Weight Ratio")
plt.title("Constraint Diagram")
plt.legend()
plt.show()

print(f"The wing area is {W_0/WS:.2f} sq ft")
print(f"The aircraft thrust is {W_0*TW_Ratio:.2f} lbs")