import geopandas as gpd
import pandas as pd
import csv
import urllib.request
import codecs
import datetime
import json
from bokeh.io import output_notebook, show, output_file, export_png
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from selenium import webdriver
import imageio
import os
from pygifsicle import optimize

import fiona
shape = fiona.open('Map-Data/ne_110m_admin_0_countries.shp')
print(shape.schema)
first = shape.next()
print(first) # (GeoJSON format)
print('\n\n')
shape = fiona.open('./Countries_WGS84/Countries_WGS84.shp')
print(shape.schema)

#{'geometry': 'LineString', 'properties': OrderedDict([(u'FID', 'float:11')])}
#first feature of the shapefile
first = shape.next()
print(first) # (GeoJSON format)
#{'geometry': {'type': 'LineString', 'coordinates': [(0.0, 0.0), (25.0, 10.0), (50.0, 50.0)]}, 'type': 'Feature', 'id': '0', 'properties': OrderedDict([(u'FID', 0.0)])}
