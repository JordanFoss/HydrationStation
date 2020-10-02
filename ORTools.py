from __future__ import print_function
from ortools.linear_solver import pywraplp

# Create the mip solver with the CBC backend.
solver = pywraplp.Solver.CreateSolver('Irrigation Assets', 'CBC')

#Sets
IAssets = ["Walking Irrigator", "Centre Pivot Irrigator"]

#Currently each timestep is a day
TimeSteps = [i for i in range(365*20)]

IA = range(len(IAssets))
T = range(len(TimeSteps))

#Data
#6 megalitres per hectare per year, so this is dependent on time step chosen
WaterLevel = [6000/365 for t in T]

#Water distribution per hour for irrigation asset
WaterDisHour = [1110, 1110]

#Cost of the irrigation asset
CostOfAssets = [43000, 119000]

#KW cost of run asset per hour
EnergyCostHour = [30, 18.5]

#Cost of labour for running the machine
LabourCostHour = [30.5 for i in IA]

#Variables

# x and y are binary variables
#1 if that irrigation asset is purchased; 0 otherwise
x = [solver.IntVar(0.0, 1.0, 'x_' + str(i)) for i in IA]

#1 if we are using irrigation asset i at timestep t
y = [[solver.IntVar(0.0, 1.0, 'y_[' + str(i) + ',' + str(t) + ']') for i in IA] for t in T]

print('Number of variables =', solver.NumVariables())

#Objective Function

solver.Minimize(sum(y[t][i]*(LabourCostHour[i] + EnergyCostHour[i]) for i in IA for t in T)
                + sum(x[i]*CostOfAssets[i] for i in IA))

#Constraints
#Can only use equipment we purchased
for t in T:
    for i in IA:
        solver.Add(y[t][i] <= x[i])
        
#Must meet the water require for the period
for t in T:
    for i in IA:
        solver.Add(y[t][i]*WaterDisHour[i] >= WaterLevel[t])

print('Number of constraints =', solver.NumConstraints())

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    for i in IA:
        if x[i].solution_value() > 0.9:
            print('Irrigation asset', IAssets[i], 'is purchased.')
            for t in T:
                if y[t][i].solution_value() > 0.9:
                    print(IAssets[i], 'used in day', TimeSteps[t], 'of', 365*20)
else:
    print('The problem does not have an optimal solution.')
