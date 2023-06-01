from pyomo.solvers.tests.mip.test_asl import mock_all
#from input_data_hardcoded import *
from input_data import *
from pulp import *

modelMinCost = LpProblem("MinCost", LpMinimize)

sMeansTrip = [(m, t) for t in sTrips for m in sMeans]
sMeansMeans2Trip = [(m, m2, t) for m in sMeans for m2 in sMeans for t in sTrips[:len(sTrips)-1]]

# Variables
v01MeansForTrip = LpVariable.dicts("TripWithMeans", sMeansTrip, cat=LpBinary)
v01SwitchExists = LpVariable.dicts("SwitchExists", sMeansMeans2Trip, cat=LpBinary)
vTotalCost = LpVariable ("TotalCost")

# Constraints
# One and only one means per trip
for t in sTrips:
    modelMinCost += sum(v01MeansForTrip[m,t] for m in sMeans) == 1, "SingleMeansPerTrip" + str(t)

# Switch exists
for i in sMeansMeans2Trip:
    modelMinCost += v01MeansForTrip[i[0], i[2]] + v01MeansForTrip[i[1], sTrips[sTrips.index(i[2])+1]] <= \
    1 + v01SwitchExists[i[0], i[1], i[2]], "SwitchExists"+ str(i[0]) + str(i[1]) + str(i[2])

# Only one switch possible
for t in  sTrips[:len(sTrips)-1]:
    modelMinCost += sum(v01SwitchExists[m, m2, t] for m in sMeans for m2 in sMeans) == 1, "OnlyOneSwitch" \
                    + str(t)

# Total cost
modelMinCost += vTotalCost == sum(v01MeansForTrip[m,t]*pTripCosts[m,t] for m in sMeans for t in sTrips) \
                + sum(v01SwitchExists[i]*pSwitchCosts[i[0],i[1]] for i in sMeansMeans2Trip)


#Objective
modelMinCost += vTotalCost

#Optimize
modelMinCost.solve()


print ("Total cost %f" % vTotalCost.varValue)

for t in sTrips:
    for m in sMeans:
        if v01MeansForTrip[m,t].varValue == 1:
            print("%s with %s" %(t, m))

for i in [i2 for i2 in sMeansMeans2Trip if i2[0]!= i2[1] and v01SwitchExists[i2].varValue == 1]:
    print ("Switch after %s, from %s to %s" %(i[2], i[0], i[1]))