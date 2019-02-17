# porder: Simple CLI for Planet ordersV2 API &nbsp; [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Use%20porder%20CLI%20with%20@planetlabs%20new%20ordersv2%20API&url=https://github.com/samapriya/porder)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2567466.svg)](https://doi.org/10.5281/zenodo.2567466)
[![PyPI version](https://badge.fury.io/py/porder.svg)](https://badge.fury.io/py/porder)
![Build Status](https://img.shields.io/badge/dynamic/json.svg?label=downloads&url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fporder%2Frecent%3Fperiod%3Dmonth&query=%24.data.last_month&colorB=blue&suffix=%2fmonth)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


[Ordersv2 is the next iteration of Planet's API](https://planet-platform.readme.io/docs) in getting Analysis Ready Data (ARD) delivered to you. Orders v2 allows you to improved functionality in this domain, including capability to submit an number of images in a batch order, and perform operations such as top of atmospheric reflectance, compression, coregistration and also enhanced notifications such as email and webhooks. Based on your access you can use this tool to chain together a sequence of operations. This tool is a command line interface that allows you to interact with the ordersv2 API along with place orders and download orders as needed. The tool also allows you to chain multiple processes together and additional functionalities will be added as needed. For exporting to cloud storages release 0.0.8 onwards has a configuration folder with config yml structures to be used with this tool. Simply replaces the fields as needed.

If you find this tool useful, star and cite it as below

```
Samapriya Roy. (2019, February 17). samapriya/porder: porder: Simple CLI for Planet ordersV2 API (Version 0.1.7).
Zenodo. http://doi.org/10.5281/zenodo.2567466
```

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [porder Ordersv2 Simple Client](#porder-ordersv2-simple-client)
    * [porder quota](#porder-quota)
    * [base64](#base64)
    * [idlist](#idlist)
    * [difflist](#difflist)
    * [idsplit](#idsplit)
    * [order](#order)
    * [download](#download)
    * [multipart download](#multipart-download)
    * [multiprocessing download](#multiprocessing-download)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have tested this only on python 2.7.15 but it should run on python 3.

Shapely is notoriously difficult as a library to install on windows machines so follow the steps mentioned from [Shapely’s PyPI package page](https://pypi.org/project/Shapely/). You can download and install from the [Unofficial Wheel files from here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) download depending on the python version you have. You will get a wheel file or a file ending with .whl. You can now simply browse to the folder or migrate to it in your command prompt , for example in my case I was running Python 2.7.15 and win32 version so the command was

```pip install Shapely-1.6.4.post1-cp27-cp27m-win32.whl```

Or you can use [anaconda to install](https://conda-forge.github.io/). Again, both of these options are mentioned on [Shapely’s Official PyPI page](https://pypi.org/project/Shapely/)

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

```
usage: porder [-h]
              {quota,base64,idlist,difflist,idsplit,order,ordersize,download,multipart,multiproc}
              ...

Ordersv2 Simple Client

positional arguments:
  {quota,base64,idlist,difflist,idsplit,order,ordersize,download,multipart,multiproc}
    quota               Prints your Planet Quota Details
    base64              Base 64 encode a JSON file
    idlist              Get idlist using geometry & filters
    difflist            Checks the difference between local files and
                        available Planet assets
    idsplit             Splits ID list incase you want to run them in small
                        batches
    order               Place an order & get order url currently supports
                        "toar","clip","composite","reproject","compression"
    ordersize           Estimate total download size
    download            Downloads all files in your order
    multipart           Uses multiprocessing to download for all files in your
                        order
    multiproc           Multiprocess based downloader based on satlist

optional arguments:
  -h, --help            show this help message and exit

```

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `porder idlist -h`. If you didn't install porder, then you can run it just by going to *porder* directory and running `python porder.py [arguments go here]`

## porder Simple CLI for Planet ordersv2 API
The tool is designed to simplify using the ordersv2 API and allows the user to chain together tools and operations for multiple item and asset types and perform these operations and download the assets locally.

### porder quota
Just a simple tool to print your planet subscription quota quickly.

```
usage: porder quota [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### base64
This does exactly as it sounds, it encodes your credential files to base64 for use with gcs.

```
usage: porder.py base64 [-h] --cred CRED

optional arguments:
  -h, --help   show this help message and exit

Required named arguments.:
  --cred CRED  Path to GCS credential file
```

### idlist
Create an idlist for your geometry based on some basic filters,including geometry, start and end date and cloud cover. If no cloud cover is specified everything form 0 to 100% cloud cover is included. For now the tool can handle geojson,json and kml files. The output is a csv file and an intermediate text file is also created with same idlist to help format the output csv file. The tool also allows you to make sure you get percentage overlap, when selecting image, for clip operations adjust it accordingly (usally --ovp 1 for orders not to fail during clip)

```
usage: porder idlist [-h] --input INPUT --start START --end END --item ITEM
                     --asset ASSET --number NUMBER --outfile OUTFILE
                     [--cmin CMIN] [--cmax CMAX]

optional arguments:
  -h, --help         show this help message and exit

Required named arguments.:
  --input INPUT      Input geometry file for now geojson/json/kml
  --start START      Start date in format YYYY-MM-DD
  --end END          End date in format YYYY-MM-DD
  --item ITEM        Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc
  --asset ASSET      Asset Type analytic, analytic_sr,visual etc
  --number NUMBER    Total number of assets, give a large number if you are
                     not sure
  --outfile OUTFILE  Output csv file, written as csv as well as text file

Optional named arguments:
  --cmin CMIN        Minimum cloud cover
  --cmax CMAX        Maximum cloud cover
  --overlap OVERLAP  Percentage overlap of image with search area range
                     between 0 to 100
```

A simple setup would be
```
porder idlist --input "C:\johndoe\geometry.geojson" --start "2017-01-01" --end "2018-12-31" --item "PSScene4Band" --asset "analytic_sr" --number 800 --outfile "C:\johndoe\orderlist.csv" --overlap 1
```

### difflist
It is possible you already downloaded some images or metadata files, and your you want a difference idlist to create orders for only assets and item types you do not have. It takes in your local folder path, type image or metadata and some basic filters,including geometry, start and end date and cloud cover. If no cloud cover is specified everything form 0 to 100% cloud cover is included. For now the tool can handle geojson,json and kml files. The output is a csv file and an intermediate text file is also created with same idlist to help format the output csv file.

```
usage: porder difflist [-h] --folder FOLDER --typ TYP --input INPUT --item
                          ITEM --asset ASSET --start START --end END --outfile
                          OUTFILE [--cmin CMIN] [--cmax CMAX]

optional arguments:
  -h, --help         show this help message and exit

Required named arguments.:
  --folder FOLDER    local folder where image or metadata files are stored
  --typ TYP          File type image or metadata
  --input INPUT      Input boundary to search (geojson, json)
  --item ITEM        Planet Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc
  --asset ASSET      Asset Type analytic, analytic_sr,visual etc
  --start START      Start Date YYYY-MM-DD
  --end END          End Date YYYY-MM-DD
  --outfile OUTFILE  Full path to text file with difference ID list

Optional named arguments:
  --cmin CMIN        Minimum cloud cover
  --cmax CMAX        Maximum cloud cover

```

A simple setup would be
```
porder diffcheck --folder "F:\johndoe\ps4b_xml" --typ "metadata" --input "F:\johndoe\grid.geojson" --item "PSScene4Band" --asset "analytic_sr" --start "2018-06-01" --end "2018-08-01" --cmin 0 --cmax 0.9 --outfile "F:\johndoe\diff.txt"
```

or without the cloud filter

```
porder diffcheck --folder "F:\johndoe\ps4b_xml" --typ "metadata" --input "F:\johndoe\grid.geojson" --item "PSScene4Band" --asset "analytic_sr" --start "2018-06-01" --end "2018-08-01" --outfile "F:\johndoe\diff.txt"
```

### idsplit
This allows you to split your idlist into small csv files incase you wanted to created batches of orders.

```
usage: porder idsplit [-h] [--idlist IDLIST] [--lines LINES] [--local LOCAL]

optional arguments:
  -h, --help       show this help message and exit
  --idlist IDLIST  Idlist file to split
  --lines LINES    Maximum number of lines in each split files
  --local LOCAL    Output folder where split files will be exported
```

A simple setup would be
```
porder idsplit --idlist "C:\johndone\orderlist.csv" --lines "100" --local "C:\johndoe\split"
```

### order
This tool allows you to actually place the order using the idlist that you created earlier. the ```--op``` argument allows you to take operations, delivery and notifications in a sequence for example ```--op toar clip email``` performs Top of Atmospheric reflectance, followed by clipping to your geometry and send you an email notification once the order has completed, failed or had any any change of status. You can now add some predefined indices for PlanetScope 4 band items with a maximum of 5 indices for a single setup . This is experimental. The list of indices include

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


```
usage: porder order [-h] --name NAME --idlist IDLIST --item ITEM --asset ASSET
                    [--boundary BOUNDARY] [--projection PROJECTION]
                    [--kernel KERNEL] [--compression COMPRESSION] [--aws AWS]
                    [--azure AZURE] [--gcs GCS] [--op OP [OP ...]]

optional arguments:
  -h, --help            show this help message and exit

Required named arguments.:
  --name NAME           Order Name to be Submitted
  --idlist IDLIST       CSV or text idlist with item IDs
  --item ITEM           Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc
  --asset ASSET         Asset Type analytic, analytic_sr,visual etc

Optional named arguments:
  --boundary BOUNDARY   Boundary/geometry for clip operation geojson|json|kml
  --projection PROJECTION
                        Projection for reproject operation of type "EPSG:4326"
  --kernel KERNEL       Resampling kernel used "near", "bilinear", "cubic",
                        "cubicspline", "lanczos", "average" and "mode"
  --compression COMPRESSION
                        Compression type used for tiff_optimize tool,
                        "lzw"|"deflate"
  --aws AWS             AWS cloud credentials config yml file
  --azure AZURE         Azure cloud credentials config yml file
  --gcs GCS             GCS cloud credentials config yml file
  --op OP [OP ...]      Add operations, delivery & notification clip|toar|comp
                        osite|zip|compression|projection|kernel|aws|azure|gcs|
                        email <Choose indices from>:
                        ndvi|gndvi|bndvi|ndwi|tvi|osavi|evi2|sr

```

A simple setup with Top of Atmospher reflectance and a few indices along with email notification would be

```
porder order --name "test-order" --idlist "path to idlist.txt" --item "PSScene4Band" --asset "analytic" --op toar ndvi ndwi evi2
```

![order](/images/placing_order.gif)

### download
The allows you to download the files in your order, to a local folder. It uses the order url generated using the orders tool to access and download the files.

```
usage: porder download [-h] [--url URL] [--local LOCAL] [--ext EXT]

optional arguments:
  -h, --help     show this help message and exit
  --url URL      order url you got for your order
  --local LOCAL  Output folder where ordered files will be exported

Optional named arguments:
  --ext EXT      File Extension to download
```

### multipart download
The allows you to multipart download the files in your order, this uses a multiprocessing downloader to quickly download your files to a local folder. It uses the order url generated using the orders tool to access and download the files.

```
usage: porder multipart [-h] [--url URL] [--local LOCAL]
                            [--errorlog ERRORLOG]

optional arguments:
  -h, --help           show this help message and exit
  --url URL            order url you got for your order
  --local LOCAL        Output folder where ordered files will be exported

Optional named arguments:
  --ext EXT      File Extension to download
```

### multiprocessing download
The uses the multiprocessing library to quickly download your files to a local folder. It uses the order url generated using the orders tool to access and download the files and includes an expotential rate limiting function to handle too many requests. To save on time it uses an extension filter so for example if you are using the zip operation you can use ".zip" and if you are downloading only images, udm and xml you can use ".tif" or ".xml" accordingly.

```
usage: porder multiproc [-h] [--url URL] [--local LOCAL] [--ext EXT]

optional arguments:
  -h, --help     show this help message and exit
  --url URL      Ordersv2 order link
  --local LOCAL  Local Path to save files

Optional named arguments:
  --ext EXT      File Extension to download

```

A simple setup would be

```porder multiproc --url "https://api.planet.com/compute/ops/orders/v2/b498ed28-f6c1-4f77-ae2b-f8a6ba325431" --local "C:\planet_demo\ps" --ext ".xml"```

## Changelog

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
