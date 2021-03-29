# Simplify geometry

This reduces the number of vertices for a multi vertex and complex GeoJSON. Extremely high vertex count (over 500) seem to fail and hence this tool allows you to export a new geojson with reduced vertices. It uses an implementation of the Visvalingam-Wyatt line simplification algorithm. This tool does work with and without Fiona, but Fiona installation is recommended.

![porder_simplify](https://user-images.githubusercontent.com/6677629/69601775-5a961700-0fe3-11ea-8eaf-3bc678babb09.gif)
