#!/usr/bin/env python

from shodan import WebAPI
SHODAN_API_KEY = "YOUR-KEY-HERE"

api = WebAPI(SHODAN_API_KEY)

# Wrap the request in a try/ except block to catch errors
try:
        # Search Shodan
        results = api.search('apache')

        # Show the results
        print 'Results found: %s' % results['total']
        for result in results['matches']:
                print 'IP: %s' % result['ip']
                print result['data']
                print ''
except Exception, e:
        print 'Error: %s' % e
