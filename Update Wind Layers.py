import arcpy
import arcgis
import zipfile
import os
import sys
# sys.path
# sys.path.append('/arcgis/home')
# import OverwriteFS

from arcgis.gis import GIS
gis = GIS("home")

arcpy.env.overwriteOutput = True

# Define Variables
project_area = 'Project_Area'
project_area_URL = 'https://services.arcgis.com/2DbqGRRQS9wbBetw/ArcGIS/rest/services/VAonShore100mOffShore200nm/FeatureServer/0'
DOD_offshore_wind_mission = 'DOD_Offshore_Wind_Mission'
DOD_offshore_wind_mission_URL = 'https://coast.noaa.gov/arcgis/rest/services/MarineCadastre/OceanEnergy/MapServer/4'
DOD_offshore_wind_mission_item = 'cf4d97019cc743bc9aa245820e9e4ce4'

# Define Constants
HOME = r"C:\temp"
CLIP_LAYER = HOME + "\\" + "Project_Area.shp"

def get_project_area (name, URL):
    rest = arcgis.features.FeatureLayer(URL)
    query = rest.query(return_all_records=True)
    file = name + ".shp"
    query.save(HOME, file)

def download_feature_layer(name, URL, item):
    rest = arcgis.features.FeatureLayer(URL)
    query = rest.query(return_all_records=True)
    file = name + ".shp"
    query.save(HOME, file)
    in_layer = HOME + "\\" + file
    out_layer = HOME + "\\" + "ODU_Wind_" + file
    arcpy.analysis.Clip(in_layer, CLIP_LAYER, out_layer)
    SHP_NAME = os.path.splitext(out_layer)[0]
    lista_files = [SHP_NAME + ".cpg",SHP_NAME + ".dbf",SHP_NAME + ".prj",SHP_NAME + ".sbn",SHP_NAME + ".sbx",SHP_NAME + ".shp",SHP_NAME + ".shp.xml",SHP_NAME + ".shx"]
    with zipfile.ZipFile(SHP_NAME + '.zip', 'w') as zipMe:
        for file in lista_files:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
            #os.remove(file)
    # OverwriteFS.overwriteFeatureService(item, SHP_NAME + ".zip")

def download_map_service(name, URL, item):
    rest = arcgis.mapping.MapServiceLayer(URL)
    query = rest.query(return_all_records=True)
    file = name + ".shp"
    query.save(HOME, file)
    in_layer = HOME + "\\" + file
    out_layer = HOME + "\\" + "ODU_Wind_" + file
    arcpy.analysis.Clip(in_layer, CLIP_LAYER, out_layer)
    SHP_NAME = os.path.splitext(out_layer)[0]
    lista_files = [SHP_NAME + ".cpg",SHP_NAME + ".dbf",SHP_NAME + ".prj",SHP_NAME + ".sbn",SHP_NAME + ".sbx",SHP_NAME + ".shp",SHP_NAME + ".shp.xml",SHP_NAME + ".shx"]
    with zipfile.ZipFile(SHP_NAME + '.zip', 'w') as zipMe:
        for file in lista_files:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
            #os.remove(file)
    # OverwriteFS.overwriteFeatureService(item, SHP_NAME + ".zip")

def create_DOD_group():
    # Define Variables
    dod_fgdb = 'DOD_Group.gdb'
    dod_fgdb_loc = HOME + '\\' + dod_fgdb
    in_features1 = HOME + '\\' + 'ODU_Wind_' + DOD_offshore_wind_mission + '.shp'
    print("Creating " + dod_fgdb)
    arcpy.management.CreateFileGDB(HOME, dod_fgdb,"CURRENT")
    print("Adding " + in_features1)
    arcpy.conversion.FeatureClassToFeatureClass(in_features1, dod_fgdb_loc, DOD_offshore_wind_mission)

get_project_area(project_area, project_area_URL)
download_map_service(DOD_offshore_wind_mission, DOD_offshore_wind_mission_URL, DOD_offshore_wind_mission_item)
create_DOD_group()


