#This lists contains all trips and all means
sTrips = ['Trip1','Trip2','Trip3','Trip4']
sMeans=['Rail', 'Road', 'Air']

#pCostTrip contains costs for assgining every trip to every means of transport
pTripCosts = {('Rail', 'Trip1'): 30, ('Rail', 'Trip2'): 25, ('Rail', 'Trip3'): 40, ('Rail', 'Trip4'): 60, ('Road', 'Trip1'): 25,
           ('Road', 'Trip2'): 40, ('Road', 'Trip3'): 45, ('Road', 'Trip4'):  50, ('Air', 'Trip1'): 40, ('Air', 'Trip2'): 20,
           ('Air', 'Trip3'): 50, ('Air', 'Trip4'): 45}
print ('Cost per trip: ', pTripCosts)

#pCostTrip contains costs for switching from one means to another means of transport at then end of every trip:
pSwitchCosts = {('Rail', 'Rail'): 0, ('Rail', 'Road'): 5, ('Rail', 'Air'): 12, ('Road', 'Rail'): 8, ('Road', 'Road'): 0,
             ('Road', 'Air'): 10, ('Air', 'Rail'): 15, ('Air', 'Road'): 10, ('Air', 'Air'): 0}