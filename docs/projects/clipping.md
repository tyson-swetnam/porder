# Clipping images

These are the steps needed to clip images to a given geometry file.

1. Create or convert your geometry into a geojson file, using [geojson.io](http://geojson.io/#map=2/20.0/0.0)
2. Use porder idlist tool to get the idlist file that intersects your geometry.
3. Place your order with clipping including as an operation and the geometry included as a the boundary file notice the **--boundary** argument passed while placing the order.

The order setup will look like the following

![clipping](https://user-images.githubusercontent.com/6677629/70329931-80ed5b00-180a-11ea-9ddd-8af67d451eae.gif)
