#!/usr/bin/python
# -*- coding: utf-8 -*-
import shapefile
import geopandas as gpd
import os


def shp2gj(folder, export):
    for items in os.listdir(folder):
        if items.endswith('.shp'):
            inD = gpd.read_file(os.path.join(folder,items))
            #Reproject to EPSG 4326
            try:
                data_proj = inD.copy()
                data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=4326)
                data_proj.to_file(os.path.join(export,str(items).replace('.shp', '.geojson')), driver="GeoJSON")
                print('Export completed to '+str(os.path.join(export,str(items).replace('.shp', '.geojson'))))
            except Exception as e:
                print(e)
#shp2gj(folder=r"C:\Users\samapriya\Downloads\nexgengrid",export=r"C:\planet_demo")
