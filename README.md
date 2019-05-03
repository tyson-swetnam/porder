# porder: Simple CLI for Planet ordersV2 API &nbsp; [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Use%20porder%20CLI%20with%20@planetlabs%20new%20ordersv2%20API&url=https://github.com/samapriya/porder)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2653983.svg)](https://doi.org/10.5281/zenodo.2653983)
[![PyPI version](https://badge.fury.io/py/porder.svg)](https://badge.fury.io/py/porder)
![Build Status](https://img.shields.io/badge/dynamic/json.svg?label=downloads&url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fporder%2Frecent%3Fperiod%3Dmonth&query=%24.data.last_month&colorB=blue&suffix=%2fmonth)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


[Ordersv2 is the next iteration of Planet's API](https://developers.planet.com/docs/orders/) in getting Analysis Ready Data (ARD) delivered to you. Orders v2 allows you to improved functionality in this domain, including capability to submit an number of images in a batch order, and perform operations such as top of atmospheric reflectance, compression, coregistration and also enhanced notifications such as email and webhooks. Based on your access you can use this tool to chain together a sequence of operations. This tool is a command line interface that allows you to interact with the ordersv2 API along with place orders and download orders as needed. The tool also allows you to chain multiple processes together and additional functionalities will be added as needed. For exporting to cloud storages release 0.0.8 onwards has a configuration folder with config yml structures to be used with this tool. Simply replaces the fields as needed.

If you find this tool useful, star and cite it as below

```
Samapriya Roy. (2019, April 30). samapriya/porder: porder: Simple CLI for Planet ordersV2 API (Version 0.2.8). Zenodo.
http://doi.org/10.5281/zenodo.2653983
```

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [porder Ordersv2 Simple Client](#porder-ordersv2-simple-client)
    * [porder quota](#porder-quota)
    * [base64](#base64)
    * [shape to geojson](#shape-to-geojson)
    * [simplify](#simplify)
    * [idlist](#idlist)
    * [difflist](#difflist)
    * [idsplit](#idsplit)
    * [order](#order)
    * [ordersize](#ordersize)
    * [concurrent](#concurrent)
    * [download](#download)
    * [multipart download](#multipart-download)
    * [multiprocessing download](#multiprocessing-download)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have tested this only on python 2.7.15 but it should run on python 3.

Shapely is notoriously difficult as a library to install on windows machines so follow the steps mentioned from [Shapely’s PyPI package page](https://pypi.org/project/Shapely/). You can download and install from the [Unofficial Wheel files from here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) download depending on the python version you have. You will get a wheel file or a file ending with .whl. You can now simply browse to the folder or migrate to it in your command prompt , for example in my case I was running Python 2.7.15 and win32 version so the command was

```pip install Shapely-1.6.4.post1-cp27-cp27m-win32.whl```

Or you can use [anaconda to install](https://conda-forge.github.io/). Again, both of these options are mentioned on [Shapely’s Official PyPI page](https://pypi.org/project/Shapely/). **Fiona** is a recommended install used by the simplify tool, but it is not necessary. You can find installation instructions [here](https://pypi.org/project/Fiona/1.8.6/#description)

Once you have shapely configured. To install **porder: Simple CLI for Planet ordersv2 API** you can install using two methods

```pip install porder```

on Ubuntu I found it helps to specify the pip type and use sudo

```sudo pip2 install porder or sudo pip3 install porder```

or you can also try

```
git clone https://github.com/samapriya/porder.git
cd porder
python setup.py install
```
For linux use sudo.

Installation is an optional step; the application can be also run directly by executing porder.py script. The advantage of having it installed is being able to execute porder as any command line tool. I recommend installation within virtual environment. If you don't want to install, browse into the porder folder and try ```python porder.py``` to get to the same result.


## Getting started

Make sure you initialized planet client by typing ```planet init``` or ```export``` or ```set PL_API_KEY=Your API Key``` As usual, to print help:

![porder_cli](https://user-images.githubusercontent.com/6677629/56938475-23549b80-6ad0-11e9-8941-e288e6a274b5.png)

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `porder idlist -h`. If you didn't install porder, then you can run it just by going to *porder* directory and running `python porder.py [arguments go here]`

## porder Simple CLI for Planet ordersv2 API
The tool is designed to simplify using the ordersv2 API and allows the user to chain together tools and operations for multiple item and asset types and perform these operations and download the assets locally.

### porder quota
Just a simple tool to print your planet subscription quota quickly.

![porder_quota](https://user-images.githubusercontent.com/28806922/53096751-d19afe00-34ed-11e9-9e10-b2c894800cbe.png)

### base64
This does exactly as it sounds, it encodes your credential files to base64 for use with gcs.

![porder_base64](https://user-images.githubusercontent.com/28806922/53096754-d495ee80-34ed-11e9-980d-418601bc975a.png)

### shape to geojson
This tool allows you to convert from  a folder with multiple shapefiles to a folder with geojson that can then be used with the tool. It makes use of geopandas and reprojects your shapefile to make it compatible while passing onto the API for search and download.

![porder_shp2geojson](https://user-images.githubusercontent.com/6677629/56938418-d1137a80-6acf-11e9-9e03-953ae367445f.png)

### simplify
This reduces the number of vertices for a multi vertex and complex GeoJSON. Extremely high vertex count (over 500) seem to fail and hence this tool allows you to export a new geojson with reduced vertices. It uses an implementation of the Visvalingam-Wyatt line simplification algorithm. This tool does work with and without Fiona, but Fiona installation is recommended.

![porder simplify](https://user-images.githubusercontent.com/6677629/56763793-36ced200-6771-11e9-8b61-8f94b1f61152.png)

### idlist
Create an idlist for your geometry based on some basic filters,including geometry, start and end date and cloud cover. If no cloud cover is specified everything form 0 to 100% cloud cover is included. For now the tool can handle geojson,json and kml files. The output is a csv file with ids. The tool also allows you to make sure you get percentage overlap, when selecting image, for clip operations adjust it accordingly (usally --ovp 1 for orders not to fail during clip). The tool now also prints estimated area in Square kilometes for the download and estimated area if you clipped your area with the geometry you are searching (just estimates).

**I have changed the setup to now do the following two things**

* The number option is optional, so it can look for all images in the time range, but be careful if the area is too large, _use at own risk_. A better option is to supply the number.

* It is possible to often forget about the different asset types, so you can now not pass an item and the script will return every possible type of asset for each item type depending on the bundle.

![porder_idlist](https://user-images.githubusercontent.com/25802584/55653649-2e602880-57bd-11e9-9d43-3587d2021d6f.png)

A simple setup would be
![porder_idlist_setup](https://user-images.githubusercontent.com/28806922/53096128-6e5c9c00-34ec-11e9-9ddd-767f96d603b0.png)

### difflist
It is possible you already downloaded some images or metadata files, and your you want a difference idlist to create orders for only assets and item types you do not have. It takes in your local folder path, type image or metadata and some basic filters,including geometry, start and end date and cloud cover. If no cloud cover is specified everything form 0 to 100% cloud cover is included. For now the tool can handle geojson,json and kml files. The output is a csv file with ids.

![porder_difflist](https://user-images.githubusercontent.com/25802584/54535868-dc6a7680-4965-11e9-8047-250c568f10e1.png)

A simple setup would be
![porder_diffcheck_setup](https://user-images.githubusercontent.com/28806922/53096408-14100b00-34ed-11e9-8ee1-8c49e8145aef.png)

or without the cloud filter

![porder_diffcheck_nocloud_setup](https://user-images.githubusercontent.com/28806922/53096598-8a147200-34ed-11e9-8583-8ceaa93da65d.png)

### idsplit
This allows you to split your idlist into small csv files incase you wanted to created batches of orders.

![porder_idsplit](https://user-images.githubusercontent.com/25802584/54536155-877b3000-4966-11e9-9a32-9a4379eef0f7.png)

A simple setup would be
![porder_idsplit_setup](https://user-images.githubusercontent.com/28806922/53097536-b204d500-34ef-11e9-8a6c-e2d52986d90c.png)

### order
This tool allows you to actually place the order using the idlist that you created earlier. the ```--op``` argument allows you to take operations, delivery and notifications in a sequence for example ```--op toar clip email``` performs Top of Atmospheric reflectance, followed by clipping to your geometry and send you an email notification once the order has completed, failed or had any any change of status. You can now add some predefined indices for PlanetScope 4 band items with a maximum of 5 indices for a single setup . This is experimental. The list of indices include

<center>

Index             | Source                                                                        |
------------------|-------------------------------------------------------------------------------|
Simple ratio (SR) | [Jordan 1969](https://esajournals.onlinelibrary.wiley.com/doi/abs/10.2307/1936256)
Normalized Difference Vegetation Index (NDVI) | [Rouse et al 1973](https://ntrs.nasa.gov/search.jsp?R=19740022614)
Green Normalized Difference Index (GNDVI) | [Gitelson et al 1996](https://www.sciencedirect.com/science/article/abs/pii/S0034425796000727)
Blue Normalized Difference Vegetation Index (BNDVI) | [Wang et al 2007](https://www.sciencedirect.com/science/article/pii/S1672630807600274)
Transformed Vegetation Index (TVI) | [Broge and Leblanc 2000](https://www.sciencedirect.com/science/article/abs/pii/S0034425700001978)
Optimized Soil Adjusted Vegetation Index (OSAVI) | [Rondeaux et al 1996](https://www.sciencedirect.com/science/article/abs/pii/0034425795001867)
Enhanced Vegetation Index (EVI2) | [Jian et al 2008](https://www.sciencedirect.com/science/article/abs/pii/S0034425708001971)
Normalized Difference Water Index (NDWI) | [Gao 1996](https://www.sciencedirect.com/science/article/abs/pii/S0034425796000673)
Modified Soil-adjusted Vegetation Index v2 (MSAVI2) | [Qi 1994](https://www.sciencedirect.com/science/article/abs/pii/0034425794901341?via%3Dihub)

</center>

![porder_order](https://user-images.githubusercontent.com/25802584/54535982-25bac600-4966-11e9-9638-b3d9453119be.png)

A simple setup with image clip with email notification would be

![porder_clip_email](https://user-images.githubusercontent.com/28806922/53097227-f5ab0f00-34ee-11e9-88ce-fc3f776df2de.png)

The same setup with delivery of each image, its metadata as a zip file would be. Note how we only added zip to the op list

![porder_clip_zip_email](https://user-images.githubusercontent.com/28806922/53097313-29863480-34ef-11e9-9bf0-b4883b82f682.png)

A simple setup with Top of Atmospher reflectance and a few indices along with email notification would be

![porder_index_email](https://user-images.githubusercontent.com/28806922/53097451-7a962880-34ef-11e9-8dcf-2173174fb0cc.png)

![order](/images/placing_order.gif)

### ordersize
The tool now allows you to estimate the total download size for a specific order.

![porder_ordersize](https://user-images.githubusercontent.com/28806922/53097620-e4163700-34ef-11e9-893b-73551d485c83.png)

An example setup look like the following

<center>

![ordersize](/images/ordersize.png)

</center>

### concurrent
The tool allows you to check on number of running orders, to get at limit for concurrent orders.

![porder_concurrent](https://user-images.githubusercontent.com/6677629/54481442-ffccde80-480a-11e9-89fa-32e288fd2ea1.png)

### download
The allows you to download the files in your order, to a local folder. It uses the order url generated using the orders tool to access and download the files.

![porder_download](https://user-images.githubusercontent.com/28806922/53097694-11fb7b80-34f0-11e9-92bd-3b841ab8b3df.png)

### multipart download
The allows you to multipart download the files in your order, this uses a multiprocessing downloader to quickly download your files to a local folder. It uses the order url generated using the orders tool to access and download the files.

![porder_multipart](https://user-images.githubusercontent.com/28806922/53097736-2b042c80-34f0-11e9-9724-68e9ed356ab7.png)

### multiprocessing download
The uses the multiprocessing library to quickly download your files to a local folder. It uses the order url generated using the orders tool to access and download the files and includes an expotential rate limiting function to handle too many requests. To save on time it uses an extension filter so for example if you are using the zip operation you can use ".zip" and if you are downloading only images, udm and xml you can use ".tif" or ".xml" accordingly.

![porder_multiprocessing](https://user-images.githubusercontent.com/28806922/53097786-4707ce00-34f0-11e9-9e79-78ba1d4ba27c.png)

A simple setup would be

![porder_multiproc_setup](https://user-images.githubusercontent.com/28806922/53097885-71f22200-34f0-11e9-88dd-c60c9cd03f6c.png)

## Changelog

### v0.3.0
- Enhances idlist to execute faster search and return using Planet CLI
- Included better error handling while placing order.

### v0.2.8
- Added tool to convert folder with shapefiles to GeoJSONs

### v0.2.7
- Improved overlap calculations for larger geometries
- Added a geometry simplification tool to reduce number of vertices

### v0.2.6
- Skysat area are calculated using EPSG:3857 to resolve metadata EPSG issue
- General improvements

### v0.2.5
- Fixed issue with area calculation estimates
- General improvements

### v0.2.4
- Now functions without limit on the number of assets in the idlist
- Parses possible asset types if only item type is supplied for idlist

### v0.2.3
- Now estimates area before and after clip when you run idlist
- General improvements

### v0.2.1
- Now exports only csv idlist
- Fixed count with concurrency check

### v0.2.0
- Fixed pysmartdl install issues
- Added concurrent orders check
- version and os resolve for shapely

### v0.1.9
- Added msavi
- Fixed issues with GeoJSON read

### v0.1.8
- Fixed issues with empty JSON append
- General improvements to the tool

### v0.1.7
- Added band math indices for PlanetScope item
- Fixed issues with retry for downloader
- General improvements to the tool

### v0.1.6
- Made fixes to have python 3.X compatability

### v0.1.5
- General improvements and bug fixes

### v0.1.4
- Fixed issue with Python 3 CSV write compatability
- Fixed issues with Shapely instance issue

### v0.1.3
- Fixed issue with clipboard access in headless setup

### v0.1.2
- Fixed issue and extension for multiprocessing downloader
- Overall general improvements to the tool

### v0.1.0
- Fixed issue and improved idlist and sort
- Fixed issue with clip tool
- Overall general improvements to the tool

### v0.0.8
- Improvements to operations in order tool
- Now supports export to gcs/azure/aws along with kernel, projection and compression
- base64 encoding tool for encoding gcs credentials
- Overall general improvements to the tool

### v0.0.7
- Now allows for all downloads or download using extension
- Polling for order to complete and automatically download
- General improvements

### v0.0.6
- Merged contribution by David Shean
- Fixed issues with op equals None
- Fixed issues with relative import
- Improved Py3 compatability
- General improvements

### v0.0.5
- Added exponential backoff for pydl
- Fixed issues with dependency
- General overall improvements

### v0.0.4
- Created strict geoinstersection to avoid orders to fail
- Improvements to overlap function
- General overall improvements

### v0.0.3
- Added overlap function to idlist
- Added multiprocessing downloader with rate limit and extension filter
- General overall improvements

### v0.0.2
- Fixed issues with import modules
