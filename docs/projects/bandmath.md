# Band Math on Clipped Images

These are the steps needed to clip images to a given geometry file.

1. Create or convert your geometry into a geojson file, using [geojson.io](http://geojson.io/#map=2/20.0/0.0)
2. Use porder idlist tool to get the idlist file that intersects your geometry.
3. Place your order with clipping including as an operation and the geometry included as a the boundary file notice the **--boundary** argument passed while placing the order. Bandmath is passed as operations here we pass **ndvi ndwi evi2** after the clipping operation in the same order setup.

Read about [available indices here](https://samapriya.github.io/porder/projects/order/). Pass index names in lowercase **ndvi ndwi evi2 sr tvi** and you can pass a maximum of 5 indices at a time. *Your capability to perform this operation is based on your overall permission*

The order setup will look like the following

![clipping_index](https://user-images.githubusercontent.com/6677629/70330242-2d2f4180-180b-11ea-82f6-c6807477687f.gif)
