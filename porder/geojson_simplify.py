import visvalingamwyatt as vw
import json


# get coordinates list depth
def list_depth(dic, level=1):
    counter = 0
    str_dic = str(dic)
    if "[[[[" in str_dic:
        counter += 1
    return(counter)


def geosimple(inp,output,num):
    try:
        import fiona
        shape = fiona.open(inp)
        with open(inp) as aoi:
            aoi_resp = json.load(aoi)
            if list_depth(aoi_resp['features'][0]['geometry']['coordinates'])==0:
                print('Number of current vertices '+str(len(aoi_resp['features'][0]['geometry']['coordinates'][0])))
            elif list_depth(aoi_resp['features'][0]['geometry']['coordinates'])==1:
                print('Number of current vertices '+str(len(aoi_resp['features'][0]['geometry']['coordinates'][0][0])))
            else:
                print('Please check GeoJSON: Could not parse coordinates')
        with fiona.Env():
            with fiona.open(inp, 'r') as src:
               with fiona.open(output, 'w', schema=src.schema, driver=src.driver, crs=src.crs) as sink:
                for f in src:
                    sink.write(vw.simplify_feature(f, number=num))
            print('Write Completed to: '+str(output))
    except ImportError:
        with open(inp) as aoi:
            aoi_resp = json.load(aoi)
            if list_depth(aoi_resp['features'][0]['geometry']['coordinates'])==0:
                aoi_geom = aoi_resp['features'][0]['geometry']['coordinates']
                print('Number of current vertices '+str(len(aoi_resp['features'][0]['geometry']['coordinates'][0])))
            elif list_depth(aoi_resp['features'][0]['geometry']['coordinates'])==1:
                aoi_geom = aoi_resp['features'][0]['geometry']['coordinates'][0]
                print('Number of current vertices '+str(len(aoi_resp['features'][0]['geometry']['coordinates'][0][0])))
            else:
                print('Please check GeoJSON: Could not parse coordinates')
        ft = {
          "type": "Feature",
          "geometry": {
            "type": "Polygon",
            "coordinates": []
          },
          "properties": {
            "vertex_count": num
          }
        }
        ft['geometry']['coordinates']=aoi_geom
        #returns a copy of the feature, simplified (using number of vertices)
        b= vw.simplify_feature(ft, number=num)
        ft['geometry']['coordinates']=b['geometry']['coordinates']
        with open(output, 'w') as g:
            json.dump(ft, g)
        print('Write Completed to: '+str(output))
#geomsimple(inp=r'C:\Users\samapriya\Downloads\vertex.geojson',output=r'C:\Users\samapriya\Downloads\v2.geojson',num=5)
