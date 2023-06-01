#from input_data import *
from input_data_hardcoded import *
from pyomo.environ import*

# Creating the model
m = AbstractModel()

# Sets
m.sTrips = Set()
m.sTripsButLast = Set()
m.sMeans = Set()
m.sMeansMeans2Trip = Set(dimen=3)
m.sSwitchExistsDomain = Set(dimen=4)

# Paramters
m.pTripCosts = Param(m.sMeans, m.sTrips, mutable=True)
m.pSwitchCosts = Param(m.sMeans, m.sMeans, mutable=True)

# Variables
m.v01MeansForTrip = Var(m.sMeans, m.sTrips, within=Binary)
m.v01SwitchExists = Var(m.sMeansMeans2Trip, within=Binary)
m.vTotalCost = Var(within=NonNegativeReals)

# Constraints
def fcSingleMeansPerTrip (model, t):
    return sum(model.v01MeansForTrip[m1, t] for m1 in model.sMeans) == 1


def fcSwitchExists (model, m1, m2, t1, t2):
    return model.v01MeansForTrip[m1, t1] + model.v01MeansForTrip[m2, t2] <= 1 + model.v01SwitchExists[m1, m2, t1]


def fcOnlyOneSwitch (model, t):
    return sum(model.m.v01SwitchExists[m1, m2, t] for m1 in model.sMeans for m2 in model.sMeans) == 1


def fcTotalCost (model):
    return model.vTotalCost == sum(model.v01MeansForTrip[m1, t]*model.pTripCosts[m1, t] for m1 in model.sMeans for t in model.sTrips) \
           + sum(model.v01SwitchExists[i[0], i[1], i[2]] * model.pSwitchCosts[i[0], i[1]] for i in model.sMeansMeans2Trip)


def fobj_expression(model):
    return model.vTotalCost

sTripsButLast = sTrips[:len(sTrips)-1]
sMeansMeans2Trip = [(m, m2, t) for m in sMeans for m2 in sMeans for t in sTrips[:len(sTrips)-1]]
sSwitchExistsDomain = [(m, m2, t, sTrips[sTrips.index(t)+1]) for m in sMeans for m2 in sMeans
                       for t in sTripsButLast]


input_data = {None:{
    'sMeans': {None: sMeans},
    'sTrips': {None: sTrips},
    'sSwitchExistsDomain': {None: sSwitchExistsDomain},
    'sMeansMeans2Trip': {None: sMeansMeans2Trip},
    'pTripCosts': pTripCosts,
    'pSwitchCosts': pSwitchCosts
}}

# Model definition. Constraints
m.cSingleMeansPerTrip = Constraint(m.sTrips, rule=fcSingleMeansPerTrip)
m.cSwitchExists = Constraint(m.sSwitchExistsDomain, rule=fcSwitchExists)
m.cOnlyOneSwitch = Constraint(m.sTripsButLast, rule=fcOnlyOneSwitch)
m.cTotalCost = Constraint(rule=fcTotalCost)

# Model definition. Objective function
m.fObj = Objective(rule=fobj_expression, sense=minimize)

# Creating the model
instance = m.create_instance(input_data)

# Solving the model
opt = SolverFactory('gurobi')
results = opt.solve(instance)
print(results)

print("Total cost %s" % instance.vTotalCost.value)

for (t, m) in [(trip, means) for trip in instance.sTrips for means in instance.sMeans if instance.v01MeansForTrip[means, trip].value]:
    print("Trip %s with means %s" % (t, m))

for i in [i2 for i2 in instance.sMeansMeans2Trip if i2[0] != i2[1] and instance.v01SwitchExists[i2].value == 1]:
    print("Switch after %s, from %s to %s" % (i[2], i[0], i[1]))

