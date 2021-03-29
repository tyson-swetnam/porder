# Multiprocessing or Async Downloading

The uses the multiprocessing library to quickly download your files to a local folder. It uses the order url generated using the orders tool to access and download the files and includes an expotential rate limiting function to handle too many requests. To save on time it uses an extension filter so for example if you are using the zip operation you can use ".zip" and if you are downloading only images, udm and xml you can use ".tif" or ".xml" accordingly. For python 3.4 or higher, this switches to using an true async downloader instead of using multiprocessing.

![porder_multiproc](https://user-images.githubusercontent.com/6677629/69604918-c92ba280-0fec-11ea-813d-c9ec9dc6221d.gif)
