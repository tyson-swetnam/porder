# Using zip

These are the steps needed to clip images to a given geometry file.

1. Create or convert your geometry into a geojson file, using [geojson.io](http://geojson.io/#map=2/20.0/0.0)
2. Use porder idlist tool to get the idlist file that intersects your geometry.
3. Place your order with clipping including as an operation and the geometry included as a the boundary file notice the **--boundary** argument passed while placing the order. We pass the argument **zip** to zip all files for each asset and **zipall** to zip all files into a single zip file. Use the **zipall** tool carefully, extremely large single zip files may fail depending on the overall size.

The order setup will look like the following

![clipping_zip](https://user-images.githubusercontent.com/6677629/70330738-25bc6800-180c-11ea-9c51-22999cca12db.gif)
