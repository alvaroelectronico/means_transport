from gurobipy import*
#import gurobipy



print('Cost per change: ', pCostChange)

model = Model('means_transport')

#This dictionary will be used to build the variables refering to what means of transport will be used for every trip
v01UseMean={}
for iTrip in sTrips:
    for iMean in sMeans:
        v01UseMean[iMean, iTrip]= model.addVar(vtype=GRB.BINARY, name = "Means_for_trip_{}_{}".format(iMean, iTrip))

#This list creates a list of lists, wehre every list es the tuple corresponding to trip1, trip2, change corresponding to
#all possible changes of means of transport. The corresponding variable will be built upon this variable.
Changes = list()
for ((iMean, iMean2), Val) in pCostChange.items():
    for iTrip in sTrips:
        if sTrips.index(iTrip)== len(sTrips)-1: continue
        Changes.append([iMean, iMean2, iTrip])
print (Changes)

model.update()
v01ChangeMeans={}
for change in Changes:
    v01ChangeMeans[change[0], change[1], change[2]] = model.addVar(vtype=GRB.BINARY, name = "Change_between_trips_{}_{}_{}".format(change[0], change[1], change[2]))

model.update()
print ('\n')
print (v01UseMean)
print(v01ChangeMeans)

#Change required
for iTrip in sTrips:
    if sTrips.index(iTrip) == len(sTrips) - 1: continue
    lhs = LinExpr()
    for iMean in sMeans:
        for iMean2 in sMeans:
            lhs += v01ChangeMeans[(iMean, iMean2, iTrip)]
    model.addConstr(lhs, GRB.EQUAL, 1, 'Change required')
    print ('Change required: ', iTrip, ' : ', lhs)

#Single mean for trip
for iTrip in sTrips:
    lhs = LinExpr()
    for iMean in sMeans:
        lhs += v01UseMean[(iMean, iTrip)]
    print ('Single means: ', iTrip, ' : ', lhs)
    model.addConstr(lhs, GRB.EQUAL, 1, 'Single means')

#Change and type consistency
for iTrip in sTrips:
    if sTrips.index(iTrip) == len(sTrips) - 1: continue
    lhs = LinExpr()
    rhs = LinExpr()
    for iMean in sMeans:
        for iMean2 in sMeans:
            lhs = v01UseMean[(iMean, iTrip)] + v01UseMean[(iMean2, sTrips[sTrips.index(iTrip)+1])]
            rhs = 2*v01ChangeMeans[(iMean, iMean2, iTrip)]
            print('Consistenty change-means :', iTrip, ' : ', lhs)
            print('Consistenty change-means :', iTrip, ' : ', rhs)
            model.addConstr(lhs, GRB.GREATER_EQUAL, rhs, 'Change-Means consistency')

#Objective
objExp = LinExpr()
for iTrip in sTrips:
    for iMean in sMeans:
        objExp+=v01UseMean[(iMean, iTrip)]*pCostTrip[(iMean, iTrip)]

for change in Changes:
    objExp+=v01ChangeMeans[(change[0], change[1], change[2])]*pCostChange[(change[0], change[1])]
print ('Ojective: ', objExp)


model.update()
model.setObjective(objExp, GRB.MINIMIZE)
model.optimize()
try:
    model.printAttr('X')
except:
    print('Something went wrong')