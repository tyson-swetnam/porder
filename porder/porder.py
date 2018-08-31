import subprocess
import argparse
from geojson2id import idl
from text_split import idsplit
from order_now import order
from downloader import download

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
        outfile=args.outfile)

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

spacing="                               "

def main(args=None):
    parser = argparse.ArgumentParser(description='Ordersv2 Simple Client')
    subparsers = parser.add_subparsers()
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
    parser_idlist.set_defaults(func=idlist_from_parser)

    parser_idsplit = subparsers.add_parser('idsplit',help='Splits ID list incase you want to run them in small batches')
    parser_idsplit.add_argument('--idlist',help='Idlist file to split')
    parser_idsplit.add_argument('--lines',help='Maximum number of lines in each split files')
    parser_idsplit.add_argument('--local',help='Output folder where split files will be exported')
    parser_idsplit.set_defaults(func=idsplit_from_parser)

    parser_order = subparsers.add_parser('order', help='Place an order & get order url currently supports "toar","clip","composite","reproject","compression"')
    required_named = parser_order.add_argument_group('Required named arguments.')
    required_named.add_argument('--name', help='Order Name to be Submitted', required=True)
    required_named.add_argument('--idlist', help='IDlist of file IDs', required=True)
    required_named.add_argument('--item', help='Item Type PSScene4Band|PSOrthoTile|REOrthoTile etc', required=True)
    required_named.add_argument('--asset', help='Asset Type analytic, analytic_sr,visual etc', required=True)
    optional_named = parser_order.add_argument_group('Optional named arguments')
    optional_named.add_argument('--boundary', help='Boundary/geometry for clip operation geojson|json|kml',default=None)
    optional_named.add_argument('--projection', help='Projection for reproject operation of type "EPSG:4326"',default=None)
    optional_named.add_argument('--kernel', help='Resampling kernel used "near", "bilinear", "cubic", "cubicspline", "lanczos", "average" and "mode"',default=None)
    optional_named.add_argument('--compression', help='Compression type used for tiff_optimize tool, "lzw"|"deflate"',default=None)
    optional_named.add_argument('--op', nargs='+',help="Add operations clip|toar|composite",default=None)

    parser_order.set_defaults(func=order_from_parser)

    parser_download = subparsers.add_parser('download',help='Downloads all files in your order')
    parser_download.add_argument('--url',help='order url you got for your order')
    parser_download.add_argument('--local',help='Output folder where ordered files will be exported')
    parser_download.add_argument('--errorlog',help='Filenames with error downloading')
    parser_download.set_defaults(func=download_from_parser)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
