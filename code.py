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

#https://stackoverflow.com/questions/16283799/how-to-read-a-csv-file-from-a-url-with-python
#tutorial: https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0
#https://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str
#https://stackoverflow.com/questions/28836781/reading-column-names-alone-in-a-csv-file/35963291
#https://github.com/bokeh/bokeh
#https://thispointer.com/python-pandas-how-to-create-dataframe-from-dictionary/

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
#print(country_names)
#print(gdf.head())
#print(gdf[gdf['country'] == 'Antarctica'])
#Drop row corresponding to 'Antarctica'
gdf = gdf.drop(gdf.index[159])


driver = webdriver.Firefox(executable_path=r'E:\Research\Corona-Visualization\Corona-History\geckodriver.exe')
driver.set_page_load_timeout(30)
driver.get("https://www.google.com/")
driver.quit()



def Visualization(dfobj):
    global gdf
    #Merge dataframes gdf and df_2016.
    merged = gdf.merge(dfobj, left_on = 'country', right_on = 'country')
    merged_json = json.loads(merged.to_json())#Convert to String like object.
    json_data = json.dumps(merged_json)

    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)

    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]

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
    p = figure(title = 'Corona Virus Spreading History', plot_height = 600 , plot_width = 950, toolbar_location = None)
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
    export_png(p, filename="plot.png")
    print("Exported")


def IntegerChecker(value):
    try:
        return(int(value))
    except Exception as e:
        return 0

def CountryMapper(country_name):
    country_name_lower = country_name.lower()
    if(country_name_lower == 'mainland china'):
        return 'China'
    return country_name

def ReadingThroughWay1(row):
    country = row['Country/Region']
    country = CountryMapper(country)
    confirmed = IntegerChecker(row['Confirmed'])
    deaths = IntegerChecker(row['Deaths'])
    recovered = IntegerChecker(row['Recovered'])
    return country, confirmed, deaths, recovered

def ReadingThroughWay2(row):
    country = row['Country_Region']
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

def UpdateData(temp_data):
    global data
    for i in temp_data:
        if(i in data):
            data[i]=temp_data[i]
        else:
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

while(current<=90):
    print("current_date = ",current_date)
    year, month, day =  FindMonthDayYear(str(current_date))
    url = base_string + month+'-'+day+'-'+year+'.csv'
    try:
        temp_data = ImportingFile(url)
        UpdateData(temp_data)
        #print("length = ",len(data),len(temp_data))
        dfObj = MakePandaDataFrame(data)
        #print(dfObj.head())
        if(current == 50):
            Visualization(dfObj)

    except Exception as e:
        print(e)
    current_date = current_date + datetime.timedelta(days=1)
    current = current+1
    if(ending_date == current_date):
        break
