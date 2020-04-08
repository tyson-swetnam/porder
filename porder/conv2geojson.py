#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import geopandas as gpd
from .kml2ee import kml2coord
import os


def convert(folder, export):
    for items in os.listdir(folder):
        if items.endswith(".shp"):
            inD = gpd.read_file(os.path.join(folder, items), encoding="utf-8")
            # Reproject to EPSG 4326
            try:
                data_proj = inD.copy()
                data_proj["geometry"] = data_proj["geometry"].to_crs(epsg=4326)
                data_proj.to_file(
                    os.path.join(export, str(items).replace(".shp", ".geojson")),
                    driver="GeoJSON",
                )
                print(
                    "Export completed to "
                    + str(os.path.join(export, str(items).replace(".shp", ".geojson")))
                )
            except Exception as e:
                print(e)
        elif items.endswith(".kml"):
            try:
                gj = kml2coord(os.path.join(folder, items))
                with open(
                    os.path.join(export, str(items).replace(".kml", ".geojson")), "w"
                ) as outfile:
                    json.dump(gj, outfile)
                print(
                    "Export completed to "
                    + str(os.path.join(export, str(items).replace(".kml", ".geojson")))
                )
            except Exception as e:
                print(e)


# shp2gj(folder=r"C:\Users\samapriya\Downloads\nexgengrid",export=r"C:\planet_demo")
