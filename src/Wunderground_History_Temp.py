# coding: utf-8
# Wunderground has a limit of 10 API calls per minute. To be on the safer side, I'll make 10 calls every 150 seconds
# So, there is a wait after every 5 calls

import urllib2
import json
import calendar as cal
import string
import time
from datetime import datetime

year = [2015]
month = [1,2,3]

target_dir = '../data/temperature/raw_data/'

for y in year:
    for m in month:
        # Let's sleep for 90 seconds before we start with the next month
        print 'Sleeping for 90 seconds ...'
        time.sleep(90)

        max_date = cal.monthrange(y, m)[1]
        for i in xrange(max_date):

            if (i+1) % 10 == 0:
                print 'Sleeping for 90 seconds ...'
                time.sleep(90)

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