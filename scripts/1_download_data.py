# -*- coding: utf-8 -*-
import sys
import os
import argparse
import json
import urllib.parse
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

def load_salons(api_key, page_size=20, limit=10000):
    API_ROOT = "http://webservice.recruit.co.jp/beauty/salon/v1/"

    def make_params(start):
        return {
            "key": api_key,
            "order": 3,
            "address": "東京",
            "start": start,
            "count": page_size,
            "format": "json"
        }

    salons = []
    index = 0
    timing = 10
    _limit = limit
    border = _limit / timing
    while index < _limit:
        # fetch salons
        p = make_params(index + 1)
        url = API_ROOT + "?" + urllib.parse.urlencode(p)
        resp = requests.get(url)

        # retrieve results
        if resp.ok:
            body = resp.json()
            if "results" in body and "salon" in body["results"]:
                results = body["results"]
                count = int(results["results_returned"])
                page = index // page_size
                max_count = int(results["results_available"])
                if max_count < _limit:
                    _limit = max_count
                    if index == 0:
                        border = _limit / timing

                # parse json to salon object
                for sj in results["salon"]:
                    salons.append(sj)

                index += count
                if index > border:
                    print("done {0} / {1}".format(index, _limit))
                    border += (_limit / timing)

            else:
                raise Exception("can not retrieve the results")
        else:
            resp.raise_for_status()

    return salons

if __name__ == "__main__":
    # for command line tool
    parser = argparse.ArgumentParser(description="Download data from hotpepper beauty api.")
    parser.add_argument("key", type=str, help="key for recruit api.")
    parser.add_argument("--limit", type=int, default=-1, help="cut under the n count word.")
    args = parser.parse_args()

    # preparation
    path = os.path.join(os.path.dirname(__file__), "../data/")
    api_key = args.key

    # extract data
    salons = []
    if args.limit < 0:
        salons = load_salons(api_key)
    else:
        salons = load_salons(api_key, limit=args.limit)

    # save as json file
    j = json.dumps(salons, indent=2, ensure_ascii=False)
    path = os.path.join(path, "salons.json")
    with open(path, "wb") as f:
        f.write(j.encode("utf-8"))
