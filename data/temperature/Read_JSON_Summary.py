import json
import pandas as pd
import os
import glob

path = os.getcwd()+"/raw_data/201*.json"
df = pd.DataFrame(columns=('date', 'fog', 'rain', 'snow', 'hail', 'thunder', 'tornado', 'meantempm', 'maxtempm', 'meanvisi', 'maxhumidity'))
i = 0

for fname in glob.glob(path):
    print "Reading file ", fname

    content = open(fname).read()
    config = json.loads(content)
    summary = config['history']['dailysummary'][0]

    mday = summary['date']['mday']
    mon = summary['date']['mon']
    year = summary['date']['year']
    date = year + '-' + mon + '-' + mday

    fog = float(summary['fog'])
    rain = float(summary['rain'])
    snow = float(summary['snow'])
    hail = float(summary['hail'])
    thunder = float(summary['thunder'])
    tornado = float(summary['tornado'])
    meantempm = float(summary['meantempm'])
    maxtempm = float(summary['maxtempm'])
    meanvisi = float(summary['meanvisi'])
    maxhumidity = float(summary['maxhumidity'])
    # precipm = float(summary['precipm'])

    obs = [date, fog, rain, snow, hail, thunder, tornado, meantempm, maxtempm, meanvisi, maxhumidity]
    df.loc[i] = obs
    i += 1 # Increment the counter

# print df
df.to_csv('weather.csv')