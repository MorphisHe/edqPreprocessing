'''
21. Identify precinct neighbors (required) (sequence diagram not required)
    - Identify two precincts as neighbors if they share a common boundary of at least 200 feet.

Approach:
    - Enlarge each precinct shape by 100 feets = 30.48 meters
    - For each enlarged precinct shape, find all others shape that it intersects and mark them as neighbors.
'''

import geopandas as gpd
import pandas as pd

METER_COORD_SYSTEM = "EPSG:3857"
GEO_COORD_SYSTEM = "EPSG:4326"
ENLARGE_SIZE = 30.48 # 30.48 meters = 100 feets
PRECINCT_FILE_PATH = "../all_states_precincts_cname_neighbor_demo.json"

def generate_neighbors(gdf): 
    gdf = gdf.to_crs(METER_COORD_SYSTEM) # convert to coordinate system that uses meters
    state_identifiers = gdf["State"].unique().tolist()
    stateGDF_with_neighbors = []
    for stateID in state_identifiers:
        cur_state_gdf = gdf[gdf["State"] == stateID]
        cur_state_gdf["enlarged_geometry"] = ""
        for index, row in cur_state_gdf.iterrows():
            cur_geometry = row["geometry"]
            cur_state_gdf.at[index, "enlarged_geometry"] = cur_geometry.buffer(ENLARGE_SIZE)
        cur_state_gdf.set_geometry("enlarged_geometry", inplace=True)

        cur_state_gdf["Neighbors"] = ""
        for index, row in cur_state_gdf.iterrows():
            cur_geometry = row["geometry"]
            cur_CName = row["CName"]
            neighbors = cur_state_gdf[cur_state_gdf["enlarged_geometry"].intersects(cur_geometry)]["CName"].tolist()
            neighbors.remove(cur_CName)
            neighbors = [cur_CName + "," + neighbor for neighbor in neighbors] # [100, 101; 100, 102; ...]
            cur_state_gdf.at[index, "Neighbors"] = "; ".join(neighbors)

        cur_state_gdf.set_geometry("geometry", inplace=True, drop=True)
        stateGDF_with_neighbors.append(cur_state_gdf)
    
    merged_gdf = pd.concat(stateGDF_with_neighbors, ignore_index=True)
    merged_gdf = merged_gdf.to_crs(GEO_COORD_SYSTEM) # convert back to original coordinate
    return merged_gdf

all_state_gdf = gpd.read_file(PRECINCT_FILE_PATH)
gdf_with_neighbors = generate_neighbors(all_state_gdf)
gdf_with_neighbors.to_file("../all_states_precincts_cname_neighbor_demo_test.json", driver="GeoJSON")