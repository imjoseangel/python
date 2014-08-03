#!/usr/bin/env python
import wolframalpha
import optparse

client = wolframalpha.Client('YOUR-KEY-HERE')

def main():
    parser = optparse.OptionParser(usage='Usage: %prog -q <query>')
    parser.add_option('-q', dest='query', type='string', help='specify query')
    (options, args) = parser.parse_args()
    if (options.query == None): 
        print parser.usage
        exit(0)
    else:
        query = options.query

    try:
        res = client.query(query)
        print(next(res.results).text)
    except:
        print '[-] There are no results to show'

if __name__ == '__main__':
    main()
