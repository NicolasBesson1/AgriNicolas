
import openrouteservice
from openrouteservice import convert
import folium
import json
import time


client = openrouteservice.Client(key='5b3ce3597851110001cf62481c10219bc06d47a9bd9024dbb4ec9931')

'''Distances entre toutes les fermes et G-SCOP'''

gscop_coord=(5.717486565975392,45.19087596124514)
payre_norbert_coord=(5.546161873015417,45.31132367189215)
vilmorin_jardin_coord=(5.096509136179054,45.64444387503803)
petite_perriere_coord=(5.632756521458269, 45.529630823265514)
ferme_colibris_coord=(5.546697107972713,45.14561006698147)
bergerie_lignare_coord=(5.98771057715641,45.05165420997515)


my_house_coord=(5.725963633012889,45.179772899650175)


locations=[gscop_coord,payre_norbert_coord,vilmorin_jardin_coord,petite_perriere_coord,ferme_colibris_coord,bergerie_lignare_coord]


distances=[[0 for _ in range(len(locations))] for _ in range(len(locations))]

for i in range(len(locations)):
    for j in range(len(locations)):
        if i!=j:
            
            res = client.directions((locations[i],locations[j]),radiuses=-1)
            distance=round(res['routes'][0]['summary']['distance']/1000,1)
            distances[i][j]=distance
            time.sleep(1.1)


with open("../data/distances.json",mode="w") as f:
    json.dump(distances,f)



points=dict()

points['G-SCOP'] = [(45.19087596124514,5.717486565975392),"46 Avenue Felix Viallet", "38000", "Grenoble"]
points['Payre Norbert'] = [(45.31132367189215,5.546161873015417), "2089 route St Quentin", "38430", "Moirans"]
points['Vilmorin Jardin'] = [(45.64444387503803,5.096509136179054),"65 rue Luzais", "38070", "Saint Quentin Fallavier"]
points['Petite Perriere'] = [(45.529630823265514,5.632756521458269),"595 route Perrières", "38480", "Pressins"]
points['Bergerie Lignare'] = [(45.05165420997515,5.98771057715641),"La Pallud", "38520", "Ornon"]

with open("../data/points.json",mode="w") as f:
    json.dump(points,f)
