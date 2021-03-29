# Place an order

This tool allows you to actually place the order using the idlist that you created earlier. the **```--op```** argument allows you to take operations, delivery and notifications in a sequence for example **```--op toar clip email```** performs Top of Atmospheric reflectance, followed by clipping to your geometry and send you an email notification once the order has completed, failed or had any any change of status. An important changes is the concept of passing bundles instead of using assets. Bundles are predefined meaning all assets in a bundle are not available for an item your attempt at downloading that attempt will fail.

For example if an item id '20181227_125554_0f4c' does not have surface reflectance asset type. So if you try to download this using bundle type analytic_sr_udm2 it will not work, similary if you order an item where a specific operation cannot be performed for example if you order visual and then try to do bandmath with four bands. These examples and more are where **fallback bundles** come in handy. Think of this as providing a list of bundles to keep trying if one bundle type fails. The priority goes left to right. You can provide comma seperated fallback bundles for example as

**```analytic_sr_udm2,analytic```** instead of **```analytic_sr_udm2```** to avoid certain items from failing to download.

The list of operations for the **```--op```** are below and **the order of these operations is important**

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
anchor  | Anchor image id for coregistration|  
format | Delivery format choose from COG/PL_NITF to use for the format tool  
gee  |  provide gee-project,gee-collection

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

![porder_order](https://user-images.githubusercontent.com/6677629/69603933-ffb3ee00-0fe9-11ea-9a54-164b01a8b25c.gif)

## Operations setup
![porder_order_operations](https://user-images.githubusercontent.com/6677629/69603872-db581180-0fe9-11ea-9975-30c4bf49f115.gif)
