import geopandas as gpd
import pandas as pd
import csv
import urllib.request
import codecs
import datetime

#https://stackoverflow.com/questions/16283799/how-to-read-a-csv-file-from-a-url-with-python
#tutorial: https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0
#https://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str
#https://stackoverflow.com/questions/28836781/reading-column-names-alone-in-a-csv-file/35963291

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

    print(len(temp_data))
    return temp_data
    #print(response.json())

def FindMonthDayYear(date_string):
    date_string = date_string.split('-')
    year = date_string[0]
    month = date_string[1]
    day = date_string[2]
    return year, month, day
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

datafile = 'CSV-Data/share-of-adults-defined-as-obese.csv'
#Read csv file using pandas
df = pd.read_csv(datafile, names = ['entity', 'code', 'year', 'per_cent_obesity'], skiprows = 1)
#print(df.head())

#print(df.info())
#print(df[df['code'].isnull()])


current=1
current_date = datetime.datetime.date(datetime.datetime.now())
base_string =  'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
while(current<=10):
    print(current_date)
    year, month, day = FindMonthDayYear(str(current_date))
    url = base_string + month+'-'+day+'-'+year+'.csv'
    try:
        ImportingFile(url)
    except Exception as e:
        print(e)
    current_date = current_date - datetime.timedelta(days=1)
    current = current+1
