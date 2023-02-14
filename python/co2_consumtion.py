
import json

with open("../data/distances.json",mode='r') as f:
    distances=json.load(f)

N=len(distances)


fuel_consumption=0.080  #kg of fuel / km
co2_emission_diesel = 3.169 #kg of CO2 / kg of fuel
co2_emission_lubricant = 0.00641 #kg of CO2 / kg of fuel

C=[[distances[i][j]*fuel_consumption*(co2_emission_diesel+co2_emission_lubricant) for i in range(N)] for j in range(N)]

for c in C:
    print(c)

with open("../data/co2_consumption.json",mode='w') as f:
    json.dump(C,f)
