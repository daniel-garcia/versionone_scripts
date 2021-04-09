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


def query(endpoint, headers, scopes, tsa_status=None, sort="order"):
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
        "Scope.Name": "$scopes",
        "Category.Name": "$types"
      },
      "with": {
        "$types": [
          "Big Story",
          "Feature"
        ],
        "$scopes": scopes
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

        l = prefix
        if l:
          l = l + ' '
        l = "%s [%s]" % (s['Name'], s['Number'])

        if s.get('Custom_TSAStatus2.Name', None) in PR_SET_DATE:
            ds = s['Custom_TSADate']
            if ds:
                ds = dateparse(ds)
                ds = ds.strftime('%m/%d/%Y')
            else:
                ds = "TBD"
            l = l + (" - %s" % ds)

        print (l)

def dump_pr(args, headers, scopes, debug=False):
    for p in pr_order:
        print ('* ', p)
        dump(query(args.endpoint, headers, scopes, pr_groupings[p], args.sort), prefix='')


def main():
    parser = argparse.ArgumentParser(description='export versionone stories.')
    parser.add_argument('--token', default=os.environ.get('VERSION_ONE_TOKEN'))
    parser.add_argument('--endpoint', default=os.environ.get('VERSION_ONE_ENDPOINT'))
    parser.add_argument('-s', '--scope', action='append', nargs='+')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--tsa_status', default=None)
    parser.add_argument('--sort', default='order')
    parser.add_argument('--output', default='text')
    args = parser.parse_args()
    headers = {}

    scopes = [x for y in args.scope for x in y]
    # print(scopes)

    if args.token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer ' + args.token

    tsa_status = None
    if args.tsa_status is not None:
        tsa_status = args.tsa_status.split(',')

    if args.output == 'text':
        dump(query(args.endpoint, headers, scopes, tsa_status, args.sort), args.debug)
    elif args.output == 'pr':
        dump_pr(args, headers, scopes, args.debug)


if __name__ == '__main__':
    main()

