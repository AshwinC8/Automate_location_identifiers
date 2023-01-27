import pandas as pd
import geocoder
from openlocationcode import openlocationcode as pluscode
import pygeohash

# Input file 
df=pd.read_csv("input.csv") 

# df['latitude'] = None
# df['longitude'] = None
# df['geohash'] = None
# df['pluscode'] = None

locations_m = []
index_m = []

for index, row in df.iterrows():
    i,j,k = row["statename"], row["Districtname"], row["officename"]

    g = geocoder.arcgis(f" {i} {j} {k} ")

    if not g.latlng :
        df.at[index, 'latitude'] = "NONE"
        df.at[index, 'longitude'] = "NONE"
        df.at[index, 'geohash'] = "NONE"
        df.at[index, 'pluscode'] = "NONE"
        locations_m.append(f"India {i} {j} {k} ")
        index_m.append(index)
        continue

    latitude = g.latlng[0]
    longitude = g.latlng[1]

    ghash = pygeohash.encode(latitude, longitude)

    pc = pluscode.encode(latitude, longitude)

    print(f"{index} {k} {latitude}, {longitude}, {pc}, {ghash}")

    df.at[index, 'latitude'] = latitude
    df.at[index, 'longitude'] = longitude
    df.at[index, 'geohash'] = ghash
    df.at[index, 'pluscode'] = pc

if  locations_m and index_m: 
    dict = {'index': index_m, 'locations': locations_m} 
    df_m = pd.DataFrame(dict)
    df_m.to_csv('exceptions.csv')

# Output file
df.to_csv('output.csv') 