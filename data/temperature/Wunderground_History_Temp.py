# coding: utf-8

import urllib2
import json
import calendar as cal
import string

year = [2016]
month = [03]

for y in year:
    for m in month:
        max_date = cal.monthrange(y, m)[1]
        for i in xrange(max_date):
            s = str(y) + string.zfill(str(m), 2) + string.zfill(str(i+1), 2)
            url = 'http://api.wunderground.com/api/0020b1868a2c32c4/history_' + s + '/q/NY/New_York.json'
            print 'Writing ' + s
            response = urllib2.urlopen(url)
            json_string = response.read()
            f = open('./raw_data/'+s+'.json', 'w')
            f.write(json_string)
            f.close()
            response.close()

print 'Complete'