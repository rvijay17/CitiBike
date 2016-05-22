########################
# Import raw CSV data, do some data manipulation
# and write the file as a Feather datafile
########################

import pandas as pd
import feather
import glob

dirname = '../../../Data/CitiBike_Data/'
# filename = '201506-citibike-tripdata.csv'
filename = '20*-citibike-tripdata.csv'
weather_file = '../data/temperature/weather.csv'
feather_output_filename = 'bikedata.feather'
public_holiday_file = 'nyc_public_holiday.csv'
listFiles = []

# Read the data files
for fname in glob.glob(dirname + filename):
    listFiles.append(pd.read_csv(fname))

bikedata = pd.concat(listFiles)
# weather = pd.read_csv(weather_file)
# weather.drop('Unnamed: 0', axis=1, inplace=True)

# Data manipulation
# Only have data where gender is either 1 or 2
bikedata = bikedata[bikedata['gender'].isin([1,2])]

# Convert gender column into male and female columns, then remove gender columns
bikedata['male'] = (bikedata.gender == 1).astype(int);
bikedata['female'] = (bikedata.gender == 2).astype(int);
bikedata.drop('gender', axis=1, inplace=True)

# Making both the keys in the dataframes of same type (<type 'datetime.date'>)
# Some files have no seconds (like 2016-06)
try:
    bikedata['dtstarttime'] = pd.to_datetime(bikedata.starttime, format="%m/%d/%Y %H:%M:%S")
except ValueError:
    bikedata['dtstarttime'] = pd.to_datetime(bikedata.starttime, format="%m/%d/%Y %H:%M")

try:
    bikedata['dtstoptime'] = pd.to_datetime(bikedata.stoptime, format="%m/%d/%Y %H:%M:%S")
except ValueError:
    bikedata['dtstoptime'] = pd.to_datetime(bikedata.stoptime, format="%m/%d/%Y %H:%M")

bikedata['date'] = bikedata.dtstarttime.dt.date.apply(lambda x:x.strftime('%Y-%m-%d'))

# Set the startdate and stopdate - minutes and seconds reset to 0 (in the following format - 2016-03-01 06:00:00)
# This has been done so that we could aggregate departures and arrivals per hour to identify bike usage
bikedata['dtstartdatehour'] = bikedata.dtstarttime.apply(lambda x:x.replace(minute=0,second=0))
bikedata['dtstopdatehour'] = bikedata.dtstoptime.apply(lambda x:x.replace(minute=0,second=0))

# df = pd.merge(bikedata, weather, on='date', how='left')
df = bikedata

# datetime.datetime columns are not supported by Feather
df.drop('dtstarttime', axis=1, inplace=True)
df.drop('dtstoptime', axis=1, inplace=True)

feather.write_dataframe(df, dirname + feather_output_filename)

print "Successfully written into feather format"