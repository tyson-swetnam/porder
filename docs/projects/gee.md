These are the steps needed to deliver your images to **Google Earth Engine**.

1. Make sure you setup your GEE & planet account first [based on these instructions](https://developers.planet.com/docs/integrations/gee/quickstart/) and create or convert your geometry into a geojson file, using [geojson.io](http://geojson.io/#map=2/20.0/0.0)
2. Use porder idlist tool to get the idlist file that intersects your geometry.
3. Place your order with gee included as an operation and the google-cloud-project,collection-name included for the **--gee** argument passed while placing the order.

*Your capability to perform this operation is based on your overall permission and if you followed the setup mentioned in steps 1.*

The order setup will look like the following

![porder_gee](https://user-images.githubusercontent.com/6677629/105747304-3cd58200-5f06-11eb-8b50-b903035c4ad2.gif)
