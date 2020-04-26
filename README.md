# porder: Simple CLI for Planet ordersV2 API &nbsp; [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Use%20porder%20CLI%20with%20@planetlabs%20new%20ordersv2%20API&url=https://github.com/samapriya/porder)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3731859.svg)](https://doi.org/10.5281/zenodo.3731859)
[![PyPI version](https://badge.fury.io/py/porder.svg)](https://badge.fury.io/py/porder)
![Build Status](https://img.shields.io/badge/dynamic/json.svg?label=downloads&url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fporder%2Frecent%3Fperiod%3Dmonth&query=%24.data.last_month&colorB=blue&suffix=%2fmonth)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


[Ordersv2 is the next iteration of Planet's API](https://developers.planet.com/docs/orders/) in getting Analysis Ready Data (ARD) delivered to you. Orders v2 allows you to improved functionality in this domain, including capability to submit an number of images in a batch order, and perform operations such as top of atmospheric reflectance, compression, coregistration and also enhanced notifications such as email and webhooks. Based on your access you can use this tool to chain together a sequence of operations. This tool is a command line interface that allows you to interact with the ordersv2 API along with place orders and download orders as needed. The tool also allows you to chain multiple processes together and additional functionalities will be added as needed. For exporting to cloud storages release 0.0.8 onwards has a configuration folder with config yml structures to be used with this tool. Simply replaces the fields as needed.

**Please note: This tool is in no way an official tool or Planet offering, but is a personal project created and maintained by Samapriya Roy**

If you use this tool to download data for your research, and find this tool useful, star and cite it as below

```
Samapriya Roy. (2020, March 28). samapriya/porder: porder: Simple CLI for Planet ordersV2 API (Version 0.6.6). Zenodo.
http://doi.org/10.5281/zenodo.3731859
```

### **[Read the Guided Docs here](https://samapriya.github.io/porder/)**
## Table of contents
* [Prerequisites](#prerequisites)
* [Installing porder](#installing-porder)
* [Windows Setup](#windows-setup)
* [Getting started](#getting-started)
* [porder Simple CLI for Planet ordersv2 API](#porder-simple-cli-for-planet-ordersv2-api)
    * [porder version](#porder-version)
    * [porder readme](#porder-readme)
    * [porder quota](#porder-quota)
    * [base64](#base64)
    * [convert to geojson](#convert-to-geojson)
    * [simplify](#simplify)
    * [idlist](#idlist)
    * [difflist](#difflist)
    * [idsplit](#idsplit)
    * [idcheck](#idcheck)
    * [bundles](#bundles)
    * [order](#order)
    * [cancel](#cancel)
    * [orderstate list](#orderstate-list)
    * [ordersize](#ordersize)
    * [stats](#stats)
    * [download](#download)
    * [multipart download](#multipart-download)
    * [multiprocessing download](#multiprocessing-download)

## Prerequisites
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying. I recommend installation within virtual environment if you are worries about messing up your current environment.

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go.

**This command line tool is dependent on shapely and fiona and as such uses functionality from GDAL**
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install python-gdal
```
For Windows I found this [guide](https://webcache.googleusercontent.com/search?q=cache:UZWc-pnCgwsJ:https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows+&cd=4&hl=en&ct=clnk&gl=us) from UCLA

Also for Ubuntu Linux I saw that this is necessary before the install

```sudo apt install libcurl4-openssl-dev libssl-dev```

## Installing porder
Once you have shapely and the other libraries configured, to install **porder: Simple CLI for Planet ordersv2 API** you can install using two methods

```pip install porder```

For linux I found it helps to specify the pip type and use --user

```
pip install porder --user

or

pip3 install porder --user
```

or you can also try

```
git clone https://github.com/samapriya/porder.git
cd porder
python setup.py install
```

## Windows Setup
Shapely and a few other libraries are notoriously difficult to install on windows machines so follow the steps mentioned here **before installing porder**. You can download and install shapely and other libraries from the [Unofficial Wheel files from here](https://www.lfd.uci.edu/~gohlke/pythonlibs) download depending on the python version you have. **Do this only once you have install GDAL**. I would recommend the steps mentioned above to get the GDAL properly installed. However I am including instructions to using a precompiled version of GDAL similar to the other libraries on windows. You can test to see if you have gdal by simply running

```gdalinfo```

in your command prompt. If you get a read out and not an error message you are good to go. If you don't have gdal try Option 1,2 or 3 in that order and that will install gdal along with the other libraries

#### Option 1:
Starting from porder v0.4.5 onwards:

Simply run ```porder -h``` after installation. This should go fetch the extra libraries you need and install them. Once installation is complete, the porder help page will show up. This should save you from the few steps below.

#### Option 2:
If this does not work or you get an unexpected error try the following commands. You can also use these commands if you simply want to update these libraries.

```
pipwin refresh
pipwin install gdal
pipwin install pyproj
pipwin install shapely
pipwin install fiona
pipwing install geopandas
```

#### Option 3
For windows first thing you need to figure out is your Python version and whether it is 32 bit or 64 bit. You can do this by going to your command prompt and typing python.

![windows_cmd_python](https://user-images.githubusercontent.com/6677629/63856293-3dfc2b80-c96f-11e9-978d-d2c1a01cfe36.PNG)

For my windows machine, I have both 32-bit python 2.7.16 and 64-bit Python 3.6.6. You can get the python version at the beginning of the highlighted lines and the 32 or 64 bit within the Intel or AMD64 within the square brackets. Your default python is the one you get by just typing python in the command line. Then download the following packages based on the information we collect about our python type in the earlier step. We use unofficial binaries to install these. This step is only needed if you are on a windows machine if you are using a setup manager like anaconda you **might** be able to avoid this setup completely

At this stage **if you were unable to install gdal then download the gdal binaries first**, install that before everything else

gdal: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)

Then follow along the following libraries
* pyproj: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj)
* shapely: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)
* fiona: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
* geopandas: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#geopandas](https://www.lfd.uci.edu/~gohlke/pythonlibs/#geopandas)

To choose the version that is correct for you use the python information you collected earlier
For example for my python 3.6.6 and AMD 64 if I was installing shapely I would choose the following, here 36 means python 3.6 and amd64 refers to the 64bit we were talking about.

```Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl```

You will get a wheel file or a file ending with .whl. You can now simply browse to the folder or migrate to it in your command prompt. Once there if I am installing for my python 3.6 the command was. At this point we will make use of our trusted package installer that comes with python called pip. Note the choice of pip or pip3 depends on your python version usually you can get the pip to use with your python by typing


```pip3 -V```

you get a readout like this

```pip 18.1 from c:\python3\lib\site-packages\pip (python 3.6)```

if you have pip just replace that with ```pip -V```

Then simply install the wheel files you downloaded using the following setup

```
pip3 install full path to Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl

in my case that would be

pip3 install "C:\Users\samapriya\Downloads\Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl"
```

Or you can use [anaconda to install](https://conda-forge.github.io/). Again, both of these options are mentioned on [Shapely’s Official PyPI page](https://pypi.org/project/Shapely/).


## Getting started

Make sure you initialized planet client by typing ```planet init```. As usual, to print help:

![pmain](https://user-images.githubusercontent.com/6677629/79036688-c0e99380-7b98-11ea-9625-ddd03d558a4f.png)

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `porder idlist -h`. If you didn't install porder, then you can run it just by going to *porder* directory and running `python porder.py [arguments go here]`

## porder Simple CLI for Planet ordersv2 API
The tool is designed to simplify using the ordersv2 API and allows the user to chain together tools and operations for multiple item and asset types and perform these operations and download the assets locally.

### porder version
This prints the tool version and escapes. Simple use would be

```
porder version
```

### porder readme
Now open the readme webpage in your browser using

```
porder readme
```

### porder quota
Just a simple tool to print your planet subscription quota quickly.

![porder_quota](https://user-images.githubusercontent.com/28806922/53096751-d19afe00-34ed-11e9-9e10-b2c894800cbe.png)

### base64
This does exactly as it sounds, it encodes your credential files to base64 for use with gcs.

![porder_base64](https://user-images.githubusercontent.com/28806922/53096754-d495ee80-34ed-11e9-980d-418601bc975a.png)

### convert to geojson
This tool allows you to convert from a folder with multiple shapefiles or kml files to a folder with geojson that can then be used with the tool. It makes use of geopandas and reprojects your shapefile to make it compatible while passing onto the API for search and download. KML conversions are handled seperately.

![pconvert](https://user-images.githubusercontent.com/6677629/79036707-f1313200-7b98-11ea-9c6b-19960d1c6923.png)

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

To run an experiment to add additional filter, you can now pass an additional string or range filter or both flag for string and range filters, a setup would be. The additional filters are optional

```
porder idlist --input "Path to geojson file" --start "YYYY-MM-DD" --end "YYYY-MM-DD" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --filters range:clear_percent:55:100 --number 20

porder idlist --input "Path to geojson file" --start "YYYY-MM-DD" --end "YYYY-MM-DD" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --filters string:satellite_id:"1003,1006,1012,1020,1038" --number 20

porder idlist --input "Path to geojson file" --start "YYYY-MM-DD" --end "YYYY-MM-DD" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --filters string:satellite_id:"1003,1006,1012,1020,1038" range:clear_percent:55:100 --number 20
```

The idlist tool can now use a multipolygon and iteratively look for scenes.

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

### idcheck
It is possible for you to modify the idlist, add or remove ids. Once done, this tool allows you to estimate the total area of images and area that intersect with your geometry or area if clipped.

![porder_idcheck](https://user-images.githubusercontent.com/6677629/57543905-c05ed200-7323-11e9-9afb-09613ffffd06.png)

A simple setup would be
![porder_idcheck_setup](https://user-images.githubusercontent.com/6677629/57543933-d5d3fc00-7323-11e9-946f-200a4791f5e8.png)

### bundles
Ordering using ordersv2 uses the concept of bundles. A bundle is a combination of multiple assets for an item that come together and are delivered as part of the overall fulfillment of the order. For example an analytic asset for PSScene4Band is a single tif file, however the analytic bundle for PSScene4Band includes analytic tiff file, the analytic_xml metadata and the udm data mask file as part of the bundle. You can find more information about [bundles here](https://developers.planet.com/docs/orders/product-bundles-reference/). Thus the concept of bundles bring together single function to order and download multiple related assets. Since the list of bundles is long, this tool simply allows you to get every bundle type based on item type. The setup is simple

![porder_bundles](https://user-images.githubusercontent.com/6677629/61171622-48da3880-a548-11e9-829f-d8c71dc39ce5.png)

A simple setup would be

```
porder bundles --item "PSScene4Band"
```

### order
This tool allows you to actually place the order using the idlist that you created earlier. the ```--op``` argument allows you to take operations, delivery and notifications in a sequence for example ```--op toar clip email``` performs Top of Atmospheric reflectance, followed by clipping to your geometry and send you an email notification once the order has completed, failed or had any any change of status. An important changes is the concept of passing bundles instead of using assets. Bundles are predefined meaning all assets in a bundle are not available for an item your attempt at downloading that attempt will fail.

For example if an item id '20181227_125554_0f4c' does not have surface reflectance asset type. So if you try to download this using bundle type analytic_sr_udm2 it will not work, similary if you order an item where a specific operation cannot be performed for example if you order visual and then try to do bandmath with four bands. These examples and more are where **fallback bundles** come in handy. Think of this as providing a list of bundles to keep trying if one bundle type fails. The priority goes left to right. You can provide comma seperated fallback bundles for example as

```analytic_sr_udm2,analytic``` instead of ```analytic_sr_udm2``` to avoid certain items from failing to download.

The list of operations for the ```--op``` are below and ** the order of these operations is important**

clip|toar|comp
                        osite|zip|zipall|compression|projection|kernel|aws|azu
                        re|gcs|email <Choose indices from>:
                        ndvi|gndvi|bndvi|ndwi|tvi|osavi|evi2|msavi2|sr

<center>

op                | description                                                                   |
------------------|-------------------------------------------------------------------------------|
clip | Clip imagery can handle single and multi polygon verify or create geojson.io
toar | Top of Atmosphere Reflectance imagery generated for imagery
harmonize| Harmonize Dove R (instrument type PS2.SD) data to classic dove (instrument type PS)
composite | Composite number of images in a given order
zip | Zip bundles together and creates downloads (each asset has a single bundle so multiple zip files)
zipall | Create a single zip file containing all assets
compression | Use image compression
projection | Reproject before downloaing image
aws | Option called to specify delivery to AWS
azure | Option called to specify delivery to AZURE
gcs | Option called to specify delivery to GCS
email | Email notification to your planet registered email

</center>


You can now add some predefined indices for PlanetScope 4 band items with a maximum of 5 indices for a single setup . This is experimental. The list of indices include

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
Normalized Difference Water Index (NDWI) | [McFeeters 1996](https://www.tandfonline.com/doi/abs/10.1080/01431169608948714)
Modified Soil-adjusted Vegetation Index v2 (MSAVI2) | [Qi 1994](https://www.sciencedirect.com/science/article/abs/pii/0034425794901341?via%3Dihub)

</center>

![porder_order](https://user-images.githubusercontent.com/6677629/61171618-48da3880-a548-11e9-9166-d0ae7b2ca0ca.png)

A simple setup with image clip with email notification would be

![porder_clip](https://user-images.githubusercontent.com/6677629/61171619-48da3880-a548-11e9-8e7c-4059866e68f5.png)

The same setup with delivery of each image, its metadata as a zip file would be. Note how we only added zip to the op list

![porder_clip_zip](https://user-images.githubusercontent.com/6677629/61171620-48da3880-a548-11e9-9c96-1d12ca762ca4.png)

A simple setup with Top of Atmospher reflectance and a few indices along with email notification would be

![porder_indices](https://user-images.githubusercontent.com/6677629/61171621-48da3880-a548-11e9-8ab9-c3a3658c7d5b.png)

### cancel
You can cancel a queued order or cancel all queued orders, before the status changes to running. Simply put you can cancel a specific order before it starts running or cancel all of your queued orders.

```
usage: porder cancel [-h] [--id ID]

optional arguments:
  -h, --help  show this help message and exit
  --id ID     order id you want to cancel use "all" to cancel all
```

Setup to cancel an order

```
porder cancel --id "orderid goes here"
```

to cancel all queued orders

```
porder cancel --id "all"
```

### orderstate list
This tool allows you to get the list of orders based on the states and based on the start and end dates of orders. For example if you want to find out all orders that failed within the week you can use this tool to check that.

```
usage: porder ostate [-h] [--state STATE] [--start START] [--end END]
                     [--limit LIMIT]

optional arguments:
  -h, --help     show this help message and exit
  --state STATE  choose state between queued| running | success | failed |
                 partial
  --start START  start date in format YYYY-MM-DD
  --end END      end date in format YYYY-MM-DD

Optional named arguments:
  --limit LIMIT  Limit the maximum table size
```

The setup to check failed orders would be for example the following, You can place a limit on the number of orders to get by using --limit

```
porder ostate --state failed --start 2019-11-01 --end 2019-11-20
```


### ordersize
The tool now allows you to estimate the total download size for a specific order.

![porder_ordersize](https://user-images.githubusercontent.com/28806922/53097620-e4163700-34ef-11e9-893b-73551d485c83.png)

An example setup look like the following

<center>

![ordersize](/images/ordersize.png)

</center>

### stats
The tool allows you to check on number of running and queued orders for both organization and user level. Using this is simple

```
porder stats
```

output should look like this:

```
Checking on all running orders...
Total queued order for organization: 0
Total running orders for organization: 1

Total queued orders for user: 0
Total running orders for user: 0
```

### download
The allows you to download the files in your order, to a local folder. It uses the order url generated using the orders tool to access and download the files.

![porder_download](https://user-images.githubusercontent.com/28806922/53097694-11fb7b80-34f0-11e9-92bd-3b841ab8b3df.png)

### multipart download
The allows you to multipart download the files in your order, this uses a multiprocessing downloader to quickly download your files to a local folder. It uses the order url generated using the orders tool to access and download the files.

![porder_multipart](https://user-images.githubusercontent.com/28806922/53097736-2b042c80-34f0-11e9-9724-68e9ed356ab7.png)

### multiprocessing download
The uses the multiprocessing library to quickly download your files to a local folder. It uses the order url generated using the orders tool to access and download the files and includes an expotential rate limiting function to handle too many requests. To save on time it uses an extension filter so for example if you are using the zip operation you can use ".zip" and if you are downloading only images, udm and xml you can use ".tif" or ".xml" accordingly. For python 3.4 or higher, this switches to using an true async downloader instead of using multiprocessing.

![porder_multiprocessing](https://user-images.githubusercontent.com/28806922/53097786-4707ce00-34f0-11e9-9e79-78ba1d4ba27c.png)

A simple setup would be

![porder_multiproc_setup](https://user-images.githubusercontent.com/28806922/53097885-71f22200-34f0-11e9-88dd-c60c9cd03f6c.png)

## Changelog

### v0.7.0
- Now estimates total download size before downloading.
- Fixed issue with downloading single archive zip files.

### v0.6.9
- Updated readme to do bulk conversion from Shapefile and KML to geojson.
- Fixed issues with bundles read and update.

### v0.6.8
- Fixed issues with direct usage of kml to get idlist.
- Combined convert tool to convert folders with shapefiles and kml to geojsons.

### v0.6.6-v0.6.7
- Fixed downloader for pipwin for [release >= 0.4.8](https://github.com/lepisma/pipwin/pull/41)
- Improved overall package installation for windows
- Check pipwin import version to get release 0.4.9

### v0.6.5
- Added bundles check function to get latest bundles from [developers page](https://developers.planet.com/docs/orders/product-bundles-reference/).

### v0.6.4
- [Pull request](https://github.com/lepisma/pipwin/pull/38) fixed issue with pipwin installation.

### v0.6.2
- Fixed issue with werkzeug and pipwin implementation.
- Changed default overlap to 0.01
- Fixed issue with YAML loader implementation.
- General improvements.

### v0.6.1
- Added cancel order and bulk cancel orders tools

### v0.6.0
- Fixed base64 encoding for GCS credentials for python 3.
- Re-release of python 3 only supported version. Use upto version 0.5.7 only for Python 2.

### v0.5.9
- No more deperecation or future warnings from pyproj [Issue 40](https://github.com/samapriya/porder/issues/40)
- `porder search` is faster
- Python 2.7 will reach the end of its life on January 1st, 2020. No more python 2 support from v0.5.9

### v0.5.8
- Handles python version while installing pipwin
- Now open readme page in browser using **porder readme**

### v0.5.7
- Fixed arg readout if no argument is passed to CLI. [Issue 39](https://github.com/samapriya/porder/issues/39).
- Updated requirements to include DateTimeRange
- Fixed issue with GDAL~=3 requirement for fiona 1.8.11 release.

### v0.5.6
- Merged [pull request 38](https://github.com/samapriya/porder/pull/38) to allow for nested delivery of zip files to cloud storage.
- Added an order state list tool.

### v0.5.5
- Better file check for skipping download requests.
- Improvements to multiprocessing and async downloader.
- General improvements to stability and performance.

### v0.5.4
- Updated bundles.json.
- Merged pull request to [update bundles](https://github.com/samapriya/porder/pull/36).

### v0.5.3
- Updated order status.
- Check existing files before attempting redirect url and download.
- Overall optimization for faster check and updated readme for fallback bundles.

### v0.5.2
- Added harmonization tool to harmonize PS2.SD to PS2.
- Improvements and error handling to quota tool
- Merged [pull request 35](https://github.com/samapriya/porder/pull/35) to keep download progress via enumerate.

### v0.5.1
- Added utf-8 encoding for shapefile to geojson conversion
- Merged [pull request 34](https://github.com/samapriya/porder/pull/34) to refresh url once expired.

### v0.4.9
- Fixed issue with gdal import for pipwin windows.
- Fixed import issue with stats endpoint.

### v0.4.8
- Replaced concurrency check with stats endpoint to get queued and running orders.
- Change pipwin cache refresh time to two weeks.

### v0.4.7
- Fixed issue with queuing state for orders and downloads.

### v0.4.6
- Handles refreshing pipwin cache and better error handling
- Fixed issue with downloading unique manifest ID for zip files.
- Updated ReadMe with improved documentation.

### v0.4.5
- Handles installation of windows specific libraries using [pipwin](https://pypi.org/project/pipwin/).
- General improvements

### v0.4.4
- Manifest files for each asset is now written in format ItemID_manifest.json to avoid skipping manifest.json common file name.
- Simple and multipart downloader now show number of items remaining during the download.
- General improvements, bundles tool now prints Bundles:Name followed by assets included in the bundle

### v0.4.3
- Fixed issues with setup.py and pyproj version.
- Improved ReadMe instructions.

### v0.4.2
- Added geometry check functionality to multipolygon with shapely self intersection [Issue 30](https://github.com/samapriya/porder/issues/30).
- For multipolygons this also performs a vertex count check and simplifies polygon to fit under 500 vertices.
- General improvements

### v0.4.1
- Fixed issue with shapely self intersection using buffer(0).
- General improvements

### v0.4.0
- Fixed issue with placing reprojection request.
- Downloader can now download partial as well as completely successful orders.
- Added retry method for rate limit during downloading
- General improvements

### v0.3.9
- Removed deprecated bundles from bundles list.
- Improved parameter description

### v0.3.7
- Added capability to pass subscription id when submitting order.

### v0.3.6
- Replaced asset in order tool with bundles.
- Created a new bundles tool to generate bundle list for an item type
- Improvements to the idlist tool now prints output as it makes progress.

### v0.3.5
- Better integration for quota tool
- Updates information while waiting for idlist
- Updated requirements

### v0.3.4
- Added async downloader for python 3.4
- Checks for existing files before spawning processes
- Better handling of multiprocessing output
- Added a quick version tool

### v0.3.3
- Fixed issue with order name when no ops are used.
- Used file basename for splitting the idlist.

### v0.3.2
- idlist tool can no use a multipolygon and iteratively look for scenes
- Orders clip tool can now handle multipolygon clip
- Added new tool zipall to handle single archive download in format ordername_date.zip

### v0.3.1
- Can now support an additional string and range filter
- Check total area and clip area estimates from any idlist using idcheck.
- General improvements to the tool.

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
