# Get your bundle type

Ordering using ordersv2 uses the concept of bundles. A bundle is a combination of multiple assets for an item that come together and are delivered as part of the overall fulfillment of the order. For example an analytic asset for PSScene is a single tif file, however the analytic_sr_udm2 bundle for PSScene includes analytic tiff file, the analytic_xml metadata and the udm2 data mask file as part of the bundle. You can find more information about [bundles here](https://developers.planet.com/docs/orders/product-bundles-reference/). Thus the concept of bundles bring together single function to order and download multiple related assets. Since the list of bundles is long, this tool simply allows you to get every bundle type based on item type. The setup is simple

![porder_bundles](https://user-images.githubusercontent.com/6677629/69602798-bf06a580-0fe6-11ea-97ef-68c654855342.gif)

A simple setup would be

<b>
```
porder bundles --item "PSScene"
```
</b>
