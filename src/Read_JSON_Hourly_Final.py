import json
import pandas as pd
import glob

source_dir = '../data/temperature/raw_data/'
target_dir = '../data/temperature/'
path = source_dir + "201*.json"
df = pd.DataFrame(columns=('date', 'temp', 'fog', 'rain', 'snow', 'hail', 'thunder', 'tornado', 'visi',
                           'dewptm', 'humidity', 'wind_speed'))
df_list = []
df_cnt = 0

for fname in glob.glob(path):
    print "Reading file ", fname
    content = open(fname).read()
    config = json.loads(content)
    observations = config['history']['observations']
    num_of_observations = len(observations)
    # print num_of_observations

    # Ideally there should be 24 observations, one per hour
    # But
    # 1. Data is missing for an hour
    # 2. One hour has more than 1 observation

    # counter for the observations in the JSON file
    i = 0
    # data frame counter. will go from 0 to 23
    cnt_hour = 0
    while cnt_hour < 24:
        year = observations[i]['date']['year']
        mon = observations[i]['date']['mon']
        mday = observations[i]['date']['mday']
        hour = observations[i]['date']['hour']
        minute = observations[i]['date']['min']
        # print i, int(hour)

        if cnt_hour == int(hour):
            # minute = '00'
            date = year + '-' + mon + '-' + mday + ' ' + hour + ':' + '00:00'
        else:
            # Comment: hour = str(i).zfill(2)
            # minute = '00'
            date = year + '-' + mon + '-' + mday + ' ' + str(cnt_hour).zfill(2) + ':' + '00:00'

        temp = observations[i]['tempm']
        fog = observations[i]['fog']
        rain = observations[i]['rain']
        snow = observations[i]['snow']
        hail = observations[i]['hail']
        thunder = observations[i]['thunder']
        tornado = observations[i]['tornado']
        visi = observations[i]['visi']
        dewptm = observations[i]['dewptm']
        humidity = observations[i]['hum']
        wind_speed = observations[i]['wspdm']
        if wind_speed == '-9999.0':
            wind_speed = 0.0

        obs = [date, temp, fog, rain, snow, hail, thunder, tornado, visi, dewptm, humidity, wind_speed]
        df.loc[df_cnt] = obs
        df_cnt += 1

        # Increment the observations counter only if current hour matches the counter
        # (cnt_hour+1 < num_of_observations) - Added when observations stop at say 9 pm and +1 because cnt_hour starts from 0
        if cnt_hour == int(hour) and i+1 < num_of_observations:
            # print '--', i, int(hour)
            i += 1

        # Whatever happens, increment cnt_hour to have 24 observations in the data frame
        cnt_hour += 1
    # df_list.append(df)

# df = pd.concat(df_list)
print df
# df = pd.concat(df_list).reset_index(drop=True)
df.fillna(0, inplace=True)
df.to_csv(target_dir + 'weather.csv')