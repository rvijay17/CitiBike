import json
import pandas as pd

content = open('../data/temperature/raw_data/20150704.json').read()
config = json.loads(content)
#print config['response']['features']['history']
observations = config['history']['observations']

df = pd.DataFrame(columns=('date', 'temp', 'humidity', 'wind_speed', 'heatindex', 'precipitation'))
for i in xrange(len(observations)):
    date = observations[i]['date']['pretty']
    temp = float(observations[i]['tempm'])
    humidity = float(observations[i]['hum'])
    wind_speed = float(observations[i]['wspdm'])
    heatindex = float(observations[i]['heatindexm'])
    precipitation = float(observations[i]['precipm'])
    obs = [date, temp, humidity, wind_speed, heatindex, precipitation]
    #obs = {'date':date, 'temp':temp, 'humidity':humidity, 'wind_speed':wind_speed, 'heatindex':heatindex, 'precipitation':precipitation}
    df.loc[i] = obs

print df