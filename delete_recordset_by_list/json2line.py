#!/usr/bin/env python

import json
# Opening JSON file
with open('list.json') as json_file:
    data = json.load(json_file)
#    print('%s %s %s' % ( data.keys()[0],data['10.172.131.211'][0],data['10.172.131.211'][1]))
    i = 0
    while i<= (len(data)-1):
        print('%s %s %s' % ( data.keys()[i],data[data.keys()[i]][0],data[data.keys()[i]][1]))
        i += 1
