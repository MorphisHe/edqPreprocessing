'''
11. Precinct renaming (required) (sequence diagram not required)
Rename precinct names to follow a standard naming scheme using a canonical name to
meaningfully represent the data. Ensure that the original name and the canonical name are both
included in the DB.

Approach:
    Precinct canonical name with be in format: state-county-precinct#
'''

import geopandas as gpd

PRECINCT_FILE_PATH = "../all_states_precincts.json"
precinct_gdf = gpd.read_file(PRECINCT_FILE_PATH)

def generate_cname(gdf):
    gdf["CName"] = ""
    for index, row in gdf.iterrows():
        cur_state = row["State"].lower()
        cur_county = row["County"].lower()
        precinct_num = row["Precinct #"].lower()
        gdf.at[index, "CName"] = cur_state + "-" + cur_county + "-" + precinct_num

generate_cname(precinct_gdf)

RI_example_cname = list(precinct_gdf[precinct_gdf["State"]=="ri"]["CName"])[:10]
VA_example_cname = list(precinct_gdf[precinct_gdf["State"]=="va"]["CName"])[:10]
TX_example_cname = list(precinct_gdf[precinct_gdf["State"]=="tx"]["CName"])[:10]

print("Examples of Rhode Island CName:\n", RI_example_cname)
print("\n\nExamples of Vriginia CName:\n", VA_example_cname)
print("\n\nExamples of Texas CName:\n", TX_example_cname)

# print(len(precinct_gdf), len(precinct_gdf["CName"].unique()))
# precinct_gdf.to_file("../all_states_Precincts_cname.json", driver="GeoJSON")