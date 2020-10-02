from __future__ import print_function
from ortools.linear_solver import pywraplp

# Create the mip solver with the CBC backend.
solver = pywraplp.Solver.CreateSolver('Irrigation Assets', 'CBC')

#Data
#6 megalitres per hectare per year, so this is dependent on time step chosen
WaterLevel = [6, 6]

#Water distribution per hour for irrigation asset
WaterDisHour = [1110, 1]

#Cost of the irrigation asset
CostOfAssets = [43000, 119000]

#KW cost of run asset per hour
EnergyCostHour = [30, 18.5]

#Cost of labour for running the machine
LabourCostHour = [30.5, 30.5]

#Sets
IAssets = ["Walking Irrigator", "Centre Pivot Irrigator"]
TimeSteps = [0]

IA = range(len(IAssets))
T = range(len(TimeSteps))

#Variables

# x and y are binary variables
#1 if that irrigation asset is purchased; 0 otherwise
x = [solver.IntVar(0.0, 1.0, 'x_' + str(i)) for i in IA]

#1 if we are using irrigation asset i at timestep t
y = [[solver.IntVar(0.0, 1.0, 'y_[' + str(i) + ',' + str(t) + ']') for i in IA] for t in T]

print('Number of variables =', solver.NumVariables())

#Objective Function

# Maximize x + 10 * y.
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
        print('x =', x[i].solution_value())
        for t in T:
            print('y =', y[t][i].solution_value())
else:
    print('The problem does not have an optimal solution.')
