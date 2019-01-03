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

import subprocess
import argparse
import os
import sys
from .geojson2id import idl
from .text_split import idsplit
from .order_now import order
from .downloader import download
from .diffcheck import checker
from .async_downloader import asyncdownload
os.chdir(os.path.dirname(os.path.realpath(__file__)))
lpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)


#Get quota for your account
def planet_quota():
    try:
        subprocess.call('python planet_quota.py',shell=True)
    except Exception as e:
        print(e)
def planet_quota_from_parser(args):
    planet_quota()

#Create ID List with structured JSON
def idlist_from_parser(args):
    idl(infile=args.input,
        start=args.start,
        end=args.end,
        item=args.item,
        asset=args.asset,
        num=args.number,
        cmin=args.cmin,
        cmax=args.cmax,
        ovp=int(args.overlap),
        outfile=args.outfile)

#Check difference from local filelist
def difflist_from_parser(args):
    checker(folder=args.folder,typ=args.typ,infile=args.input,
    item=args.item,asset=args.asset,start=args.start,end=args.end,
    cmin=args.cmin,cmax=args.cmax,outfile=args.outfile)

#Offcourse all good merge sometimes needs a split
def idsplit_from_parser(args):
    idsplit(infile=args.idlist,linenum=args.lines,
        output=args.local)

#Place the order
def order_from_parser(args):
    order(name=args.name,
        idlist=args.idlist,
        item=args.item,
        asset=args.asset,
        op=args.op,
        boundary=args.boundary,
        projection=args.projection,
        kernel=args.kernel,
        compression=args.compression)

#Download the order
def download_from_parser(args):
    download(url=args.url,
        local=args.local,
        errorlog=args.errorlog)

#Multithreaded downloader
def asyncdownload_from_parser(args):
    asyncdownload(url=args.url,
        local=args.local,
        errorlog=args.errorlog)
def multiproc_from_parser(args):
    lpath=os.path.dirname(os.path.realpath(__file__))
    subprocess.call(os.path.join(lpath, "multiproc_pydl.py ")+args.url+" "+args.local+" "+args.ext,shell=True)

spacing="                               "

def main(args=None):
    parser = argparse.ArgumentParser(description='Ordersv2 Simple Client')
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True
    parser_planet_quota = subparsers.add_parser('quota', help='Prints your Planet Quota Details')
    parser_planet_quota.set_defaults(func=planet_quota_from_parser)

    parser_idlist = subparsers.add_parser('idlist', help='Get idlist using geometry & filters')
    required_named = parser_idlist.add_argument_group('Required named arguments.')
    required_named.add_argument('--input', help='Input geometry file for now geojson/json/kml', required=True)
    required_named.add_argument('--start', help='Start date in format YYYY-MM-DD', required=True)
    required_named.add_argument('--end', help='End date in format YYYY-MM-DD', required=True)
    required_named.add_argument('--item', help='Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc', required=True)
    required_named.add_argument('--asset', help='Asset Type analytic, analytic_sr,visual etc', required=True)
    required_named.add_argument('--number', help='Total number of assets, give a large number if you are not sure', required=True)
    required_named.add_argument('--outfile', help='Output csv file, written as csv as well as text file', required=True)
    optional_named = parser_idlist.add_argument_group('Optional named arguments')
    optional_named.add_argument('--cmin', help="Minimum cloud cover")
    optional_named.add_argument('--cmax',help="Maximum cloud cover")
    optional_named.add_argument('--overlap', help="Percentage overlap of image with search area range between 0 to 100")
    parser_idlist.set_defaults(func=idlist_from_parser)

    parser_difflist = subparsers.add_parser('difflist', help='Checks the difference between local files and available Planet assets')
    required_named = parser_difflist.add_argument_group('Required named arguments.')
    required_named.add_argument('--folder', help='local folder where image or metadata files are stored', required=True)
    required_named.add_argument('--typ', help='File type image or metadata', required=True)
    required_named.add_argument('--input', help='Input boundary to search (geojson, json)', required=True)
    required_named.add_argument('--item', help='Planet Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc', required=True)
    required_named.add_argument('--asset', help='Asset Type analytic, analytic_sr,visual etc', required=True)
    required_named.add_argument('--start', help='Start Date YYYY-MM-DD', required=True)
    required_named.add_argument('--end', help='End Date YYYY-MM-DD', required=True)
    required_named.add_argument('--outfile', help='Full path to text file with difference ID list', required=True)
    optional_named = parser_difflist.add_argument_group('Optional named arguments')
    optional_named.add_argument('--cmin', help="Minimum cloud cover")
    optional_named.add_argument('--cmax',help="Maximum cloud cover")
    parser_difflist.set_defaults(func=difflist_from_parser)

    parser_idsplit = subparsers.add_parser('idsplit',help='Splits ID list incase you want to run them in small batches')
    parser_idsplit.add_argument('--idlist',help='Idlist txt file to split')
    parser_idsplit.add_argument('--lines',help='Maximum number of lines in each split files')
    parser_idsplit.add_argument('--local',help='Output folder where split files will be exported')
    parser_idsplit.set_defaults(func=idsplit_from_parser)

    parser_order = subparsers.add_parser('order', help='Place an order & get order url currently supports "toar","clip","composite","reproject","compression"')
    required_named = parser_order.add_argument_group('Required named arguments.')
    required_named.add_argument('--name', help='Order Name to be Submitted', required=True)
    required_named.add_argument('--idlist', help='CSV or text idlist with item IDs', required=True)
    required_named.add_argument('--item', help='Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc', required=True)
    required_named.add_argument('--asset', help='Asset Type analytic, analytic_sr,visual etc', required=True)
    optional_named = parser_order.add_argument_group('Optional named arguments')
    optional_named.add_argument('--boundary', help='Boundary/geometry for clip operation geojson|json|kml',default=None)
    optional_named.add_argument('--projection', help='Projection for reproject operation of type "EPSG:4326"',default=None)
    optional_named.add_argument('--kernel', help='Resampling kernel used "near", "bilinear", "cubic", "cubicspline", "lanczos", "average" and "mode"',default=None)
    optional_named.add_argument('--compression', help='Compression type used for tiff_optimize tool, "lzw"|"deflate"',default=None)
    optional_named.add_argument('--op', nargs='+',help="Add operations, delivery & notification clip|toar|composite|zip|email",default=None)

    parser_order.set_defaults(func=order_from_parser)

    parser_download = subparsers.add_parser('download',help='Downloads all files in your order')
    parser_download.add_argument('--url',help='order url you got for your order')
    parser_download.add_argument('--local',help='Output folder where ordered files will be exported')
    parser_download.add_argument('--errorlog',help='Filenames with error downloading')
    parser_download.set_defaults(func=download_from_parser)

    parser_asyncdownload = subparsers.add_parser('multipart',help='Uses multiprocessing to download for all files in your order')
    parser_asyncdownload.add_argument('--url',help='order url you got for your order')
    parser_asyncdownload.add_argument('--local',help='Output folder where ordered files will be exported')
    parser_asyncdownload.add_argument('--errorlog',help='Filenames with error downloading')
    parser_asyncdownload.set_defaults(func=asyncdownload_from_parser)

    parser_multiproc = subparsers.add_parser('multiproc',help='''Multiprocess based downloader based on satlist''')
    parser_multiproc.add_argument('--url',help='Ordersv2 order link')
    parser_multiproc.add_argument('--local',help='Local Path to save files')
    parser_multiproc.add_argument('--ext',help='Extension of file to be downloaded')
    parser_multiproc.set_defaults(func=multiproc_from_parser)
    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
