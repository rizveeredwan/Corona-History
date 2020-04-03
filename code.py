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


#https://stackoverflow.com/questions/16283799/how-to-read-a-csv-file-from-a-url-with-python
#tutorial: https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0
#https://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str
#https://stackoverflow.com/questions/28836781/reading-column-names-alone-in-a-csv-file/35963291
#https://github.com/bokeh/bokeh
#https://thispointer.com/python-pandas-how-to-create-dataframe-from-dictionary/
#https://stackoverflow.com/questions/49929374/notadirectoryerror-winerror-267-the-directory-name-is-invalid-error-while-inv

data={}

#shape file directory
shapefile = 'Map-Data/ne_110m_admin_0_countries.shp'

#Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

#Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
country_names=[]
for ind in gdf.index:
    country_names.append(gdf['country'][ind])

country_names = sorted(country_names)
conflict_resolve={}
for i in country_names:
    #print(i)
    data[i]={}
    data[i]['confirmed']=0
    data[i]['deaths']=0
    data[i]['recovered']=0

with open('conflicted_country_resolve.csv','r') as file:
    lines = file.readlines()
    ct=0
    for l in lines:
        ct=ct+1
        if(ct==1):
            continue
        s=l.strip()
        s=s.split(',')
        giv=s[0]
        map=s[1]
        conflict_resolve[giv]=map
#print(country_names)
#print(gdf.head())
#print(gdf[gdf['country'] == 'Antarctica'])
#Drop row corresponding to 'Antarctica'
gdf = gdf.drop(gdf.index[159])


driver = webdriver.Firefox(executable_path=r'E:\Research\Corona-Visualization\Corona-History\geckodriver.exe')
driver.set_page_load_timeout(30)
driver.get("https://www.google.com/")
driver.quit()

def DeleteFile(filenames):
    for filename in filenames:
        os.remove(filename)
    print("Deleted")

def MakeGIF(filenames):

    gif_path = "corona-history.gif"
    with imageio.get_writer(gif_path, mode='I',duration=0.5) as writer:
        for i in range(0,len(filenames)):
            try:
                writer.append_data(imageio.imread(filenames[i]))
            except Exception as e:
                print(e)
    writer.close()

def Visualization(dfobj,image_file_name,date_value):
    global gdf
    #Merge dataframes gdf and df_2016.
    merged = gdf.merge(dfobj, left_on = 'country', right_on = 'country')
    merged_json = json.loads(merged.to_json())#Convert to String like object.
    json_data = json.dumps(merged_json)

    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)

    #Define a sequential multi-hue color palette.
    palette = brewer['YlOrRd'][8] #YlGnBu

    #Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]

    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40)

    #Define custom tick labels for color bar.
    tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}

    #Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

    #Create figure object.
    p = figure(title = 'Corona Virus Spreading History: '+date_value, plot_height = 600 , plot_width = 950, toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    #Add patch renderer to figure.
    p.patches('xs','ys', source = geosource, fill_color = {'field' :'deaths', 'transform' : color_mapper}, line_color = 'black', line_width = 0.25, fill_alpha = 1)

    #Specify figure layout.
    p.add_layout(color_bar, 'below')

    #Display figure inline in Jupyter Notebook.
    #output_notebook()

    #Display figure.
    #show(p)
    export_png(p, filename=image_file_name)
    print("Exported")


def IntegerChecker(value):
    value=value.strip()
    try:
        return(int(value))
    except Exception as e:
        return 0

def CountryMapper(country_name):
    global conflict_resolve
    country_name_lower = country_name.lower()
    if(country_name_lower == 'mainland china'):
        return 'China'
    if(country_name in conflict_resolve):
        return conflict_resolve[country_name]
    return country_name

def ReadingThroughWay1(row):
    country = row['Country/Region'].strip()
    country = CountryMapper(country)
    confirmed = IntegerChecker(row['Confirmed'])
    deaths = IntegerChecker(row['Deaths'])
    recovered = IntegerChecker(row['Recovered'])
    return country, confirmed, deaths, recovered

def ReadingThroughWay2(row):
    country = row['Country_Region'].strip()
    country = CountryMapper(country)
    confirmed = IntegerChecker(row['Confirmed'])
    deaths = IntegerChecker(row['Deaths'])
    recovered = IntegerChecker(row['Recovered'])
    return country, confirmed, deaths, recovered


def ImportingFile(url):
    ftpstream = urllib.request.urlopen(url)
    csvfile = csv.DictReader(codecs.iterdecode(ftpstream, 'utf-8'))
    fieldnames = csvfile.fieldnames
    if('Country/Region' in fieldnames):
        way=1
    elif('Country_Region' in fieldnames):
        way=2
    else:
        way=3
        print("SHIT")
    temp_data={}
    for line in csvfile:
        if(way == 1):
            country, confirmed, deaths, recovered = ReadingThroughWay1(line)
        elif(way==2):
            country, confirmed, deaths, recovered = ReadingThroughWay2(line)
        elif(way==3):
            print("SHIT")
            continue
        if(country not in temp_data):
            temp_data[country] = {}
            temp_data[country]['confirmed']=0
            temp_data[country]['deaths']=0
            temp_data[country]['recovered']=0
        temp_data[country]['confirmed']=temp_data[country]['confirmed']+confirmed
        temp_data[country]['deaths']=temp_data[country]['deaths']+deaths
        temp_data[country]['recovered']=temp_data[country]['recovered']+recovered

    #print(len(temp_data))
    return temp_data
    #print(response.json())

def FindMonthDayYear(date_string):
    date_string = date_string.split('-')
    year = date_string[0]
    month = date_string[1]
    day = date_string[2]
    return year, month, day

conflicting_countries=[]
def UpdateData(temp_data):
    global conflicting_countries
    global data
    for i in temp_data:
        if(i in data):
            data[i]=temp_data[i]
        else:
            conflicting_countries.append(i)
            data[i]={}
            data[i]=temp_data[i]
    return

def MakePandaDataFrame(temp_data):
    frame={
        'country': [],
        'confirmed':[],
        'deaths':[],
        'recovered':[]
    }
    for i in temp_data:
        frame['country'].append(i)
        frame['confirmed'].append(temp_data[i]['confirmed'])
        frame['deaths'].append(temp_data[i]['deaths'])
        frame['recovered'].append(temp_data[i]['recovered'])

    dfObj = pd.DataFrame(frame, columns=['country', 'confirmed', 'deaths', 'recovered'])

    return dfObj


current=1
ending_date = datetime.datetime.date(datetime.datetime.now())
current_date = datetime.date(2020, 1, 22) #year, month, day
base_string =  'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
filenames=[]
while(True):
    print("current_date = ",current_date)
    year, month, day =  FindMonthDayYear(str(current_date))
    url = base_string + month+'-'+day+'-'+year+'.csv'
    try:
        temp_data = ImportingFile(url)
        UpdateData(temp_data)
        #print("length = ",len(data),len(temp_data))
        dfObj = MakePandaDataFrame(data)
        #print(dfObj.head())
        Visualization(dfObj,'Plot-'+str(current_date)+'.png',str(current_date))
        filenames.append('Plot-'+str(current_date)+'.png')

    except Exception as e:
        print(e)
    current_date = current_date + datetime.timedelta(days=1)
    current = current+1
    if(ending_date == current_date):
        break

MakeGIF(filenames)
DeleteFile(filenames)
temp=[]
for i in data:
    temp.append(i)
temp = sorted(temp)
conflicting_countries = sorted(conflicting_countries)
"""
print("conflict")
for i in conflicting_countries:
    print(i)
print("\n\ntotal")
for i in temp:
    print(i)
print("Main countires")
"""
