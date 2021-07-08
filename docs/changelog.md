# Changelog

### v0.8.4
- Resolved [Issue 49](https://github.com/tyson-swetnam/porder/issues/49)
- Download now contains manifest.json for cross checking delivery

### v0.8.3
- Fixed bundle parsing
- Updated based bundles

### v0.8.2
- [Pull request 48](https://github.com/tyson-swetnam/porder/pull/48)
- fixes typos and equations for bandmath and includes additional reference information
- increased pipwin check time to 60+ days
- added better version check and handling
- updated license date and minor fixes

### v0.8.1
- Search function can now parse date and time. Enhancement from [Issue 47](https://github.com/tyson-swetnam/porder/issues/47)
- Updated readme site to include search examples
- Stability test across python3.7 to 3.9 and for all os types
- pipwin checks cache every one month

### v0.8.0
- Added gee-integration example
- Updated readme site to include examples

### v0.7.9
- Added gee-integration tool to order
- General improvements

### v0.7.8
- Added support for multipolygon search and clip.
- Added coregistration and format tools to order
- Removed persistent version print
- Overall cleanup and general Improvements

### v0.7.7
- Removed dependency on pendulum and general cleanup.

### v0.7.6
- Now use multiple assets with the idlist tool pass assets as analytic_sr,udm2 for example to get items with both these assets.
- Updated readme.

### v0.7.5
- Fixed pipwin python path for installer.
- idlist tool now only returns standard and excludes beta and test quality.

### v0.7.4
- added smart check on partially completed order for reordering.
- completed orders can be reordered as well

### v0.7.3
- Now constantly checks for updated version incase your porder version is not updated.
- Added a reorder tool for users to reorder an exiting order or failed order.

### v0.7.1
- ID check tool now works with/without geometry, pass an idlist, and item and asset type to check.
- Order size tool is optimized for speed.
- pipwin tool uploaded to v0.5.0 to handle windows packages.
- Overall general improvements.

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
- Fixed issue with GDAL~=3 requirement for fiona 1.8.11 release

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
