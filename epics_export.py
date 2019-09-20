#!/usr/bin/env python

import os
import json
import argparse
import requests
from dateutil.parser import parse as dateparse


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
    for i in range(len(stories)):
        s = stories[i]
        if debug:
            print s
        if filter == "Required":
            ds = s['Custom_TSADate']
            if ds:
                ds = dateparse(ds)
                ds = ds.strftime('%m/%d/%Y')
            else:
                ds = "TBD"
            print ("%s, %s - Target %s" % (s['Number'],s['Name'], ds))
        else:
            print ("%s, %s" % (s['Number'],s['Name']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='export versionone stories.')
    parser.add_argument('--token', default=os.environ.get('VERSION_ONE_TOKEN'))
    parser.add_argument('--endpoint', default=os.environ.get('VERSION_ONE_ENDPOINT'))
    parser.add_argument("--scope", default="Atlas 2.6")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("tsa_status", default="")
    args = parser.parse_args()
    headers = {}

    if args.token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + args.token

    query(args.scope, args.tsa_status, args.debug)


