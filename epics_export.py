#!/usr/bin/env python3

import os
import json
import argparse
import requests
from dateutil.parser import parse as dateparse



def printCount(filter, count) :
	if filter == "DA Review Required":
		print("Big Stories requiring DA Review (%d)" % count)
	elif filter == "Done":
		print("Big Stories that have architecture completed (%d)" % count)
	elif filter == "":
		print("New Big Stories not yet reviewed (%d)" % count)
	elif filter == "Required":
		print("Big Stories requiring architecture (%d)" % count)
	elif filter == "Not Required":
		print("Big Stories that likely do not have architecture requirements (%d)" % count)
	elif filter == "Re-review":
    		print("Big Stories that are rejected will be re-reviewed (%d)" % count)
	else:
		print("Number of stories = %d" % count)

def query(scope, filter, debug=False):
    q = """
{
  "from": "Epic",
  "select": [
    "ID.Name",
    "Name",
    "Category.Name",
    "Number",
    "Custom_TSAStatus2.Name",
    "Custom_TSADate"
  ],
  "sort": [
    "+Order"
  ],
  "where": {
    "Scope.Name": "%s",
    "Custom_TSAStatus2.Name": "%s",
    "Category.Name": "Big Story"
  }
}

""" % (scope, filter)
    url = args.endpoint + '/query.v1'
    req = requests.post(url, data=q, headers=headers)
    stories = req.json()[0]
    i = 0
    printCount(filter, len(stories))
    for i in range(len(stories)):
        s = stories[i]
        if debug:
            print(s)
        if filter == "Required":
            ds = s['Custom_TSADate']
            if ds:
                ds = dateparse(ds)
                ds = ds.strftime('%m/%d/%Y')
            else:
                ds = "TBD"
            print("%s, %s - Target %s" % (s['Number'],s['Name'], ds))
        else:
            print("%s, %s" % (s['Number'],s['Name']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='export versionone stories.')
    parser.add_argument('--token', default=os.environ.get('VERSION_ONE_TOKEN'))
    parser.add_argument('--endpoint', default=os.environ.get('VERSION_ONE_ENDPOINT'))
    parser.add_argument("--scope", default="Salus 2.4")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("tsa_status", default="")
    args = parser.parse_args()
    headers = {}

    if args.token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + args.token

    query(args.scope, args.tsa_status, args.debug)


