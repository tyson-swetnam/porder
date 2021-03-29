# Package installation

For windows first thing you need to figure out is your Python version and whether it is 32 bit or 64 bit. You can do this by going to your command prompt and typing python.

![windows_cmd_python](https://user-images.githubusercontent.com/6677629/63856293-3dfc2b80-c96f-11e9-978d-d2c1a01cfe36.PNG)

For my windows machine, I have both 32-bit python 2.7.16 and 64-bit Python 3.6.6. You can get the python version at the beginning of the highlighted lines and the 32 or 64 bit within the Intel or AMD64 within the square brackets. Your default python is the one you get by just typing python in the command line. Then download the following packages based on the information we collect about our python type in the earlier step. We use unofficial binaries to install these. This step is only needed if you are on a windows machine if you are using a setup manager like anaconda you **might** be able to avoid this setup completely

At this stage **if you were unable to install gdal then download the gdal binaries first**, install that before everything else

gdal: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)

Then follow along the following libraries

* pyproj: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj)
* shapely: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)
* fiona: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
* geopandas: [https://www.lfd.uci.edu/~gohlke/pythonlibs/#geopandas](https://www.lfd.uci.edu/~gohlke/pythonlibs/#geopandas)

To choose the version that is correct for you use the python information you collected earlier
For example for my python 3.6.6 and AMD 64 if I was installing shapely I would choose the following, here 36 means python 3.6 and amd64 refers to the 64bit we were talking about.

**```Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl```**

You will get a wheel file or a file ending with .whl. You can now simply browse to the folder or migrate to it in your command prompt. Once there if I am installing for my python 3.6 the command was. At this point we will make use of our trusted package installer that comes with python called pip. Note the choice of pip or pip3 depends on your python version usually you can get the pip to use with your python by typing


**```pip3 -V```**

you get a readout like this

**```pip 18.1 from c:\python3\lib\site-packages\pip (python 3.6)```**

if you have pip just replace that with **```pip -V```**

Then simply install the wheel files you downloaded using the following setup

<b>
```
pip3 install full path to Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl
```
</b>

in my case that would be

<b>
```
pip3 install "C:\Users\samapriya\Downloads\Shapely‑1.6.4.post2‑cp36‑cp36m‑win_amd64.whl"
```
</b>

Or you can use [anaconda to install](https://conda-forge.github.io/). Again, both of these options are mentioned on [Shapely’s Official PyPI page](https://pypi.org/project/Shapely/).
