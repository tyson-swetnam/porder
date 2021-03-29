# Prerequisites
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying. I recommend installation within virtual environment if you are worries about messing up your current environment.

**```python```** and then **```pip list```**

If you get no errors and you have python 2.7.14 or higher you should be good to go.

**This command line tool is dependent on shapely and fiona and as such uses functionality from GDAL**
For installing GDAL in Ubuntu

<b>
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
```
</b>

<b>
```
sudo apt-get install gdal-bin
```
</b>

<b>
```
sudo apt-get install python-gdal
```
</b>

For Windows I found this [guide](https://webcache.googleusercontent.com/search?q=cache:UZWc-pnCgwsJ:https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows+&cd=4&hl=en&ct=clnk&gl=us) from UCLA

Also for Ubuntu Linux I saw that this is necessary before the install

<b>
```
sudo apt install libcurl4-openssl-dev libssl-dev
```
</b>
