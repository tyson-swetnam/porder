from xml.etree import ElementTree
from shapely.geometry import Polygon, Point
import json

poly_table = []

def kml2coord(filename):
    data = open(filename)
    tree = ElementTree.parse(data)
    namespace = tree.getroot().tag[1:].split("}")[0]
    placemarks = tree.findall(".//{%s}Placemark" % namespace)
    for p in placemarks:
        for d in p.findall(".//{%s}Data" % namespace):
            if d.attrib.get('name') == 'OBJECTID':
                name = d.find('.//{%s}value' % namespace).text
        coord_text = p.find('.//{%s}coordinates' % namespace).text
        coord_pairs = coord_text.split(' ')
        coords = [z.split(',')[0:2] for z in coord_pairs]
        for x in coords:
            try:
                poly_table.append([float(x[0]),float(x[1])])
            except:
                pass
        return poly_table
