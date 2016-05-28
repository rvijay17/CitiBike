# coding: utf-8
# Wunderground has a limit of 10 API calls per minute.
# To be on the safer side, I'll make 10 calls every 'sleep_for' seconds
# So, there is a wait after every 5 calls

import urllib2
import json
import calendar as cal
import string
import time
from datetime import datetime

year = [2014]
month = [3,4,5,6,7,8,9,10,11,12]

target_dir = '../data/temperature/raw_data/'
sleep_for = 75

for y in year:
    for m in month:
        # Let's sleep before we start with the next month
        print 'Sleeping for', sleep_for, 'seconds ...'
        time.sleep(sleep_for)

        max_date = cal.monthrange(y, m)[1]
        for i in xrange(max_date):

            if (i+1) % 10 == 0:
                print 'Sleeping for', sleep_for, 'seconds ...'
                time.sleep(sleep_for)

            s = str(y) + string.zfill(str(m), 2) + string.zfill(str(i+1), 2)
            url = 'http://api.wunderground.com/api/0020b1868a2c32c4/history_' + s + '/q/NY/New_York.json'
            print 'Writing ' + s
            response = urllib2.urlopen(url)
            json_string = response.read()
            f = open(target_dir + s + '.json', 'w')
            f.write(json_string)
            f.close()
            response.close()

print 'Complete'