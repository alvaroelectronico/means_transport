# Means of transport. Problem description

A load of 20 tonnes needs to be transported on a route passing through five cities, with a choice of three different modes of transport: rail, road, and air. In any of the three intermediate cities it is possible to
change the mode of transport but the load uses a single mode of transport between two consecutive cities. Table 10.9 lists the cost of transport in $ per tonne between the pairs of cities.

> Means/cost  | 1-2 | 2-3 | 3-4 | 4-5 |
> ---         | --- | --- | --- | --- |
> Rail        |  30 |  25 |  40 |  60 |
> Road        |  25 |  40 |  45 |  50 |
> Air         |  40 |  20 |  50 |  45 |

The next table (10.10) summarizes the costs for changing the mode of transport in $ per tonne. The cost
is independent of location.

>from/to     | Rail| Road| Air |
>---         | --- | --- | --- |
>Rail        |   0 |   5 |  12 |
>Road        |   8 |   0 |  10 |
>Air         |  15 |  10 |   0 |


How should we organize the transport of the load at the least cost?

# MILP formulation

## Sets

$T$: trips \\
$M$: means

## Parameters
$C^T_{mt}$: cost of assigning means $m \in M$ to trip $t \in T$ \\
$C^S_{mm'}$: cost of switching from means $m \in M$ to means $m' \in M$ 

## Variables
$x_{mt}$: if trip $t \in T$ with means $m \in M$ \\
$y_{mm`t}$: if there is a switch from means $m \in M$ to means $m' \in M$ at the end of $t \in T$ (but last trip)

## Constraints

$\sum_{m \in M} x_{mt} = 1, \,\,\, \forall t \in T$ (all trips have a emans)

$x_{mt}+x_{m't+1} \leq 1 + y_{mm`t} , \,\,\, \forall t \in T, \,  m \in M, \,  m' \in M$ but last trip (switch exists)

$\sum_{m \in M}\sum_{m' \in M}y_{mm't} = 1,\,\,\forall t \in T$ (only one switch possible)

$x_{mt} \in \{0,1\}, \, \forall m \in M, \, t \in T$
$y_{mm't} \in \{0,1\}, \, \forall m, m' \in M, \, t \in T$

## Objective function
min. $\sum_{m \in M}\sum_{t \in T}C^T_{mt}x_{mt} \\
+\sum_{m \in M}\sum_{m' \in M}\sum_{t \in T}C^S_{mm'}y_{mm't}$