########################
# Import raw CSV data, do some data manipulation
# and write the file as a Feather datafile
########################

import pandas as pd
import feather
import glob

dirname = '../../../Data/CitiBike_Data/'
filename = '201*.csv'
feather_output_filename = 'bikedata.feather'
listFiles = []

# Read the data files
for fname in glob.glob(dirname + filename):
    bikedata = pd.read_csv(fname)

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
        try:
            bikedata['dtstarttime'] = pd.to_datetime(bikedata.starttime, format="%m/%d/%Y %H:%M")
        except ValueError:
            bikedata['dtstarttime'] = pd.to_datetime(bikedata.starttime, format="%Y-%m-%d %H:%M:%S")

    # Note required as stop date is not used in the model
    # try:
    #     bikedata['dtstoptime'] = pd.to_datetime(bikedata.stoptime, format="%m/%d/%Y %H:%M:%S")
    # except ValueError:
    #     try:
    #         bikedata['dtstoptime'] = pd.to_datetime(bikedata.stoptime, format="%m/%d/%Y %H:%M")
    #     except ValueError:
    #         bikedata['dtstoptime'] = pd.to_datetime(bikedata.stoptime, format="%Y-%m-%d %H:%M:%S")

    # Set the startdate and stopdate - minutes and seconds reset to 0 (in the following format - 2016-03-01 06:00:00)
    # This has been done so that we could aggregate departures and arrivals per hour to identify bike usage
    bikedata['dtstartdatehour'] = bikedata.dtstarttime.apply(lambda x:x.replace(minute=0,second=0))

    ## dtstopdatehour is not required as stopdate is not used in the model
    # bikedata['dtstopdatehour'] = bikedata.dtstoptime.apply(lambda x:x.replace(minute=0,second=0))

    ## The following two columns are handled in the notebook itself. The new column is created after the aggregation
    # bikedata['startdatehour'] = bikedata.dtstartdatehour.apply(lambda x:x.strftime('%Y-%m-%d %H:%M:%S'))
    # bikedata['startdate'] = bikedata.dtstarttime.dt.date.apply(lambda x:x.strftime('%Y-%m-%d'))

    # datetime.datetime columns are not supported by Feather
    # So, deleting the column after pre-processing.
    # TODO: Can we do without converting the dates in the first place?
    bikedata.drop('dtstarttime', axis=1, inplace=True)
    # bikedata.drop('dtstoptime', axis=1, inplace=True)

    print fname, ' - ', len(bikedata)

    listFiles.append(bikedata)

df = pd.concat(listFiles)
print len(df)
feather.write_dataframe(df, dirname + feather_output_filename)

print "Successfully written into feather format"