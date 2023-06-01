import pandas as pd

df_trips = pd.read_csv("trips.csv", sep=';')
sTrips = [i for i in df_trips.loc[:, "Trip"]]

df_trip_costs = pd.read_csv("trip_costs.csv", sep=';')

sMeans = list(set([i for i in df_trip_costs.loc[:, 'Means']]))
pTripCosts = {(df_trip_costs.loc[i, "Means"], df_trip_costs.loc[i, "Trip"]):
                  df_trip_costs.loc[i, "Cost"] for i in range(0, df_trip_costs.shape[0])}

df_switch_costs = pd.read_csv("switch_costs.csv", sep=';')
pSwitchCosts = {(df_switch_costs.loc[i, "Means1"], df_switch_costs.loc[i, "Means2"]):
                    df_switch_costs.loc[i, "Cost"] for i in range(0, df_switch_costs.shape[0])}