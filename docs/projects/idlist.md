# Getting an idlist

Create an idlist for your geometry based on some basic filters,including geometry, start and end date and cloud cover. If no cloud cover is specified everything form 0 to 100% cloud cover is included. For now the tool can handle geojson,json and kml files. The output is a csv file with ids. The tool also allows you to make sure you get percentage overlap, when selecting image, for clip operations adjust it accordingly (usally --ovp 1 for orders not to fail during clip). The tool now also prints estimated area in Square kilometes for the download and estimated area if you clipped your area with the geometry you are searching (just estimates).

**I have changed the setup to now do the following two things**

* The number option is optional, so it can look for all images in the time range, but be careful if the area is too large, _use at own risk_. A better option is to supply the number.

* It is possible to often forget about the different asset types, so you can now not pass an item and the script will return every possible type of asset for each item type depending on the bundle.

![porder_idlist](https://user-images.githubusercontent.com/25802584/55653649-2e602880-57bd-11e9-9d43-3587d2021d6f.png)

A simple setup would be
![porder_idlist](https://user-images.githubusercontent.com/6677629/69602327-24f22d80-0fe5-11ea-8053-4de8c030ce26.gif)

To run an experiment to add additional filter, you can now pass an additional string or range filter or both flag for string and range filters, a setup would be. The additional filters are optional

<b>
  
```
porder idlist --input "Path to geojson file" --start "YYYY-MM-DD" --end "YYYY-MM-DD" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --filters range:clear_percent:55:100 --number 20

porder idlist --input "Path to geojson file" --start "YYYY-MM-DD" --end "YYYY-MM-DD" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --filters string:satellite_id:"1003,1006,1012,1020,1038" --number 20

porder idlist --input "Path to geojson file" --start "YYYY-MM-DD" --end "YYYY-MM-DD" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --filters string:satellite_id:"1003,1006,1012,1020,1038" range:clear_percent:55:100 --number 20
```

</b>

The search tool now allows the user to pass Hours , Minutes and seconds and utilizes the local timezone on the users computer to search. This including the format HH:MM:SS seperated from yyyy-mm-dd by T. An example would be the following, while noting that passing time is purely optional and you can still search by simply passing YYYY-MM-DD.

```
porder idlist --input "Path to geojson file" --start "yyyy-mm-ddTHH:MM:SS" --end "yyyy-mm-ddTHH:MM:SS" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --filters range:clear_percent:55:100 --number 20

porder idlist --input "Path to geojson file" --start "2021-01-01T14:12:10" --end "2021-03-01T16:20:20" --item "PSScene4Band" --asset "analytic" --outfile "Path to idlist.csv" --number 20
```

The idlist tool can now use a multipolygon and iteratively look for scenes.
