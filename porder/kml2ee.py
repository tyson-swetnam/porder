__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

from xml.etree import ElementTree
from shapely.geometry import Polygon, Point
import json

poly_table = []
ft = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Polygon", "coordinates": []},
        }
    ],
}


def kml2coord(filename):
    data = open(filename)
    tree = ElementTree.parse(data)
    namespace = tree.getroot().tag[1:].split("}")[0]
    placemarks = tree.findall(".//{%s}Placemark" % namespace)
    for p in placemarks:
        for d in p.findall(".//{%s}Data" % namespace):
            if d.attrib.get("name") == "OBJECTID":
                name = d.find(".//{%s}value" % namespace).text
        coord_text = p.find(".//{%s}coordinates" % namespace).text
        coord_pairs = coord_text.split(" ")
        coords = [z.split(",")[0:2] for z in coord_pairs]
        for x in coords:
            try:
                poly_table.append([float(x[0]), float(x[1])])
            except:
                pass
        ft["features"][0]["geometry"]["coordinates"] = [poly_table]
    return ft


# kml2coord(filename=r'C:\Users\samapriya\Downloads\chgaoi.kml')
