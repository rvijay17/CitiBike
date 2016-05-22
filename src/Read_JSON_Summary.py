import json
import pandas as pd
import os
import glob

source_dir = '../data/temperature/raw_data/'
target_dir = '../data/temperature/'
path = source_dir + "201*.json"
df = pd.DataFrame(columns=('date', 'fog', 'rain', 'snow', 'hail', 'thunder', 'tornado',
                           'meantempm', 'maxtempm', 'meanvisi', 'maxhumidity', 'precipm'))

for i, fname in enumerate(glob.glob(path)):
    print "Reading file ", fname

    content = open(fname).read()
    config = json.loads(content)
    summary = config['history']['dailysummary'][0]

    mday = summary['date']['mday']
    mon = summary['date']['mon']
    year = summary['date']['year']
    date = year + '-' + mon + '-' + mday

    fog = summary['fog']
    rain = summary['rain']
    snow = summary['snow']
    hail = summary['hail']
    thunder = summary['thunder']
    tornado = summary['tornado']
    meantempm = summary['meantempm']
    maxtempm = summary['maxtempm']
    meanvisi = summary['meanvisi']
    maxhumidity = summary['maxhumidity']
    precipm = summary['precipm']
    # T stands for Trace. Too small to meaningfully measure
    if precipm == 'T':
        precipm = 0.01

    obs = [date, fog, rain, snow, hail, thunder, tornado, meantempm, maxtempm, meanvisi, maxhumidity, precipm]
    df.loc[i] = obs

df.fillna(0, inplace=True)
df.to_csv(target_dir + 'weather.csv')