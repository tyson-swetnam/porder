# porder: Simple CLI for Planet ordersV2 API
Ordersv2 is the next iteration of Planet's advance in getting Analysis Ready Data delivered to you, and the orders v2 allows you to improved functionality in this domain, including capability to submit an number of images in a batch order, and perform operations such as top of atmospheric reflectance, compression, coregistration and also enhanced notifications such as email and webhooks. Based on your access you can use this tool to chain together a sequence of operations.

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [porder Ordersv2 Simple Client](#porder-ordersv2-simple-client)
    * [porder quota](#porder-quota)
    * [idlist](#idlist)
    * [idsplit](#idsplit)
    * [order](#order)
    * [download](#download)
    * [multipart download](#multipart-download)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have tested this only on python 2.7.15 but it should run on python 3.

To install **porder: Simple CLI for Planet ordersv2 API** you can install using two methods

```pip install porder```

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
usage: porder [-h] {quota,idlist,idsplit,order,download,asyncdownload} ...

Ordersv2 Simple Client

positional arguments:
  {quota,idlist,idsplit,order,download,asyncdownload}
    quota               Prints your Planet Quota Details
    idlist              Get idlist using geometry & filters
    idsplit             Splits ID list incase you want to run them in small
                        batches
    order               Place an order & get order url currently supports
                        "toar","clip","composite","reproject","compression"
    download            Downloads all files in your order
    multipart           Uses multiprocessing to download for all files in your
                        order

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `porder idlist -h`. If you didn't install porder, then you can run it just by going to *porder* directory and running `python porder.py [arguments go here]`

## porder Simple CLI for Planet ordersv2 API
The tool is designed to simplify using the ordersv2 API and allows the user to chain together tools and operations for multiple item and asset types and perform these operation and download the assets locally.

### porder quota
Just a simple tool to print your planet subscription quota quickly.

```
usage: porder quota [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### idlist
Create an idlist for your geometry based on some basic filters,including geometry, start and end date and cloud cover. If no cloud cover is specified everything form 0 to 100% cloud cover is included. For now the tool can handle geojson,json and kml files. The output is a csv file and an intermediate text file is also created with same idlist to help format the output csv file.

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
```

A simple setup would be
```
porder idlist --input "C:\johndoe\geometry.geojson" --start "2017-01-01" --end "2018-12-31" --item "PSScene4Band" --asset "analytic_sr" --number 800 --outfile "C:\johndoe\orderlist.csv"
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
This tool allows you to actually place the order using the idlist that you created earlier. the ```--op``` argument allows you to take operations, delivery and notifications in a sequence for example ```--op toar clip email``` performs Top of Atmospheric reflectance, followed by clipping to your geometry and send you an email notification once the order has completed, failed or had any any change of status.

```
usage: porder order [-h] --name NAME --idlist IDLIST --item ITEM --asset ASSET
                    [--boundary BOUNDARY] [--projection PROJECTION]
                    [--kernel KERNEL] [--compression COMPRESSION]
                    [--op OP [OP ...]]

optional arguments:
  -h, --help            show this help message and exit

Required named arguments.:
  --name NAME           Order Name to be Submitted
  --idlist IDLIST       CSV idlist with item IDs
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
  --op OP [OP ...]      Add operations, delivery & notification
                        clip|toar|composite|zip|email

```

### download
The allows you to download the files in your order, to a local folder. It uses the order url generated using the orders tool to access and download the files.

```
usage: porder download [-h] [--url URL] [--local LOCAL] [--errorlog ERRORLOG]

optional arguments:
  -h, --help           show this help message and exit
  --url URL            order url you got for your order
  --local LOCAL        Output folder where ordered files will be exported
  --errorlog ERRORLOG  Filenames with error downloading
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
  --errorlog ERRORLOG  Filenames with error downloading
```
