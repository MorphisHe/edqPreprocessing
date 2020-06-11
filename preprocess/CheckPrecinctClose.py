'''
17. Identify unclosed polygon precinct data
    - Identify any precinct boundary data for which the polygon is not closed.
    - Modify the data to close thepolygon and classify it as a possible data error for the user to confirm the correction. 
    - Store the associated data in the errors data structure for subsequent addition to the DB.

Approach:
    - if the shape is MultiPolygon:
        check for every shape inside the MultiPolygon
    - if shape is Polygon
        check if first point equals to the last point
    - all other shape is classified as unclosed
'''

import geopandas as gpd
import shapely.geometry as geometry

PRECINCT_FILE_PATH = "../all_states_precincts.json"
all_state_gdf = gpd.read_file(PRECINCT_FILE_PATH)

def detect_unclose(gdf):
    gdf["Unclosed"] = ""
    for index, row in gdf.iterrows():
        cur_geometry = row["geometry"]
        if type(cur_geometry) == geometry.multipolygon.MultiPolygon:
            for shape in cur_geometry:
                if shape.exterior.coords[0] != shape.exterior.coords[-1]:
                    gdf.at[index, "Unclosed"] = "True"
                    break
            gdf.at[index, "Unclosed"] = "False"
        elif type(cur_geometry) == geometry.polygon.Polygon:
            unclosed = "True" if cur_geometry.exterior.coords[0] != cur_geometry.exterior.coords[-1] else "False"
            gdf.at[index, "Unclosed"] = unclosed
        else:
            gdf.at[index, "Unclosed"] = "True"
    return gdf

all_state_gdf = detect_unclose(all_state_gdf)

unclosed = all_state_gdf[(all_state_gdf["State"] == "ri") & (all_state_gdf["Unclosed"] == "True")]
print("Number Of Rhode Island Precinct(s) Not Closed:", len(unclosed))

unclosed = all_state_gdf[(all_state_gdf["State"] == "tx") & (all_state_gdf["Unclosed"] == "True")]
print("Number Of Texas Precinct(s) Not Closed:", len(unclosed))

unclosed = all_state_gdf[(all_state_gdf["State"] == "va") & (all_state_gdf["Unclosed"] == "True")]
print("Number Of Virginia Precinct(s) Not Closed:", len(unclosed))