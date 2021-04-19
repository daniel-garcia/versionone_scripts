#!/usr/local/bin/python3

import os
import json
import argparse
import requests
from dateutil.parser import parse as dateparse


def printStories(filter, stories, debug):
    count = len(stories)
    if filter == "In Progress":
        print("Architecture in Progress: %d" % count)
    elif filter == "Ready for Eng Review":
        print("Ready for engineering review: %d" % count)
    elif filter == "DA Review Required":
        print("DA review required: %d" % count)
    elif filter == "Done":
        print("Done: %d" % count)
    elif filter == "":
        print("Not reviewed: %d" % count)
    elif filter == "Required":
        print("Architecture Required: %d" % count)
    elif filter == "Not Required":
        print("Architecture not required: %d" % count)
    elif filter == "Re-review":
        print("Re-review: %d" % count)
    elif filter == "Rejected":
        print("Rejected: %d" % count)
    else:
        print("Number of stories = %d" % count)

    for s in stories:
        if debug:
            print(s)
        if filter == "Required":
            ds = s['Custom_TSADate']
            if ds:
                ds = dateparse(ds)
                ds = ds.strftime('%m/%d/%Y')
            else:
                ds = "TBD"
            print("%s [%s] - Target %s" % (s['Name'], s['Number'], ds))
        else:
            print("%s [%s]" % (s['Name'], s['Number']))


def filter_stories(filter_rejected, stories):
    if filter_rejected:
        oid_filter = 'Custom_Arch_Accept_Reject:118165'
    else:
        oid_filter = 'Custom_Arch_Accept_Reject:118164'
    ret_stories = []
    for s in stories :
        accept_reject = s['Custom_ArchAcceptReject']
        if accept_reject['_oid'] == oid_filter:
            ret_stories.append(s)
    return ret_stories


def query(scope, filter, filter_review, debug=False):
    q = """
{
  "from": "Epic",
  "select": [
	"ID.Name",
	"Name",
	"Category.Name",
	"Number",
	"Custom_TSAStatus2.Name",
	"Custom_TSADate",
	"Custom_ArchAcceptReject",
	"AssetState"
  ],
  "sort": [
	"+Order"
  ],
  "where": {
	"Scope.Name": "%s",
	"Custom_TSAStatus2.Name": "%s",
	"Category.Name": "Big Story",
	"AssetState": "Active"
  }
}

""" % (scope, filter)
    url = args.endpoint + '/query.v1'
    req = requests.post(url, data=q, headers=headers)
    stories = req.json()[0]
    if filter_review == "Rejected":
        printStories('Rejected', filter_stories(True, stories), debug)
    elif filter_review == "Re-review":
        printStories('Re-review', filter_stories(False, stories), debug)
    else:
        printStories(filter, stories, debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='export versionone stories.')
    parser.add_argument('--token', default=os.environ.get('VERSION_ONE_TOKEN'))
    parser.add_argument('--endpoint', default=os.environ.get('VERSION_ONE_ENDPOINT'))
    parser.add_argument("--scope", default="Athena 3.X")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("tsa_status", default="")
    args = parser.parse_args()
    headers = {}

    if args.token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + args.token

    if args.tsa_status == "Re-review" or args.tsa_status == "Rejected":
        query(args.scope, 'Re-review', args.tsa_status, args.debug)
    else:
        query(args.scope, args.tsa_status, None, args.debug)
