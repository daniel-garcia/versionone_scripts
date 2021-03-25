#!/usr/bin/env python

import os
import json
import argparse
import requests
from dateutil.parser import parse as dateparse

sorts = { "order": "Order",
          "id": "ID" }

statuses = [
  '',
  'Required',
  'Not Required',
  'Done',
  'Re-review',
  'Ready for Eng Review',
  'DA Review Required',
  'In Progress'
]

PR_SET_DATE = ['Required']

PR_NEED_REVIEW = 'Need Review'
PR_ARCH_REQUIRED = 'Architecture Required'
PR_ARCH_COMPLETE = 'Architecture Complete'
PR_ARCH_NOT_REQUIRED = 'No Architecure Required'
PR_NO_STATUS = 'No status'

pr_groupings = {
  PR_NEED_REVIEW: ['DA Review Required', 'Re-review'],
  PR_ARCH_REQUIRED: ['Required', 'In Progress'],
  PR_ARCH_COMPLETE: ['Done', 'Ready for Eng Review'],
  PR_ARCH_NOT_REQUIRED: ['Not Required'],
  PR_NO_STATUS: ['']
}

pr_order = [PR_NEED_REVIEW, PR_ARCH_REQUIRED, PR_ARCH_COMPLETE, PR_ARCH_NOT_REQUIRED, PR_NO_STATUS ]


def query(endpoint, headers, scope, tsa_status=None, sort="order"):
    q = {
      "from": "Epic",
      "select": [
        "ID.Name",
        "Name",
        "Category.Name",
        "Number",
        "Custom_TSAStatus2.Name",
        "Custom_TSADate",
        "Custom_ArchAcceptReject.Name"
      ],
      "sort": [ "+" + sorts.get(sort, "Order") ],
      "where": {
        "Scope.Name": scope,
        "Category.Name": "$types"
      },
      "with": {
        "$types": [
          "Big Story",
          "Feature"
        ]
      }
    }

    if tsa_status is not None:
        q['where']['Custom_TSAStatus2.Name'] = '$tsa_status'
        q['with']['$tsa_status'] = tsa_status

    url = endpoint + '/query.v1'
    req = requests.post(url, data=json.dumps(q), headers=headers)
    return req.json()[0]

def dump(stories, debug=False, prefix=''):
    i = 0
    for i in range(len(stories)):
        s = stories[i]
        if debug:
            print (s)
        if s.get('Custom_TSAStatus2.Name', None) in PR_SET_DATE:
            ds = s['Custom_TSADate']
            if ds:
                ds = dateparse(ds)
                ds = ds.strftime('%m/%d/%Y')
            else:
                ds = "TBD"
            print ("%s%s, %s - %s" % (prefix, s['Number'],s['Name'], ds))
        else:
            print ("%s%s, %s" % (prefix, s['Number'],s['Name']))

def dump_pr(args, headers, debug=False):
    for p in pr_order:
        print ('* ', p)
        dump(query(args.endpoint, headers, args.scope, pr_groupings[p], args.sort), prefix='')


def main():
    parser = argparse.ArgumentParser(description='export versionone stories.')
    parser.add_argument('--token', default=os.environ.get('VERSION_ONE_TOKEN'))
    parser.add_argument('--endpoint', default=os.environ.get('VERSION_ONE_ENDPOINT'))
    parser.add_argument("--scope", default=os.getenv('VERSION_ONE_DEFAULT_SCOPE', 'Atlas'))
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--tsa_status", default=None)
    parser.add_argument("--sort", default="order")
    parser.add_argument("--output", default="text")
    args = parser.parse_args()
    headers = {}

    if args.token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + args.token

    tsa_status = None
    if args.tsa_status is not None:
        tsa_status = args.tsa_status.split(',')

    if args.output == 'text':
        dump(query(args.endpoint, headers, args.scope, tsa_status, args.sort), args.debug)
    elif args.output == 'pr':
        dump_pr(args, headers, args.debug)


if __name__ == '__main__':
    main()

