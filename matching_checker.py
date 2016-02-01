#!/bin/python

import argparse
import datetime
import urllib
import json

SOURCES_URL = "http://tvheute.mixd.tv/sources/?api_key=%s"
EPG_URL = "http://tvheute.mixd.tv/epg/program-broadcasted/DMB/%s/between/%s/%s/?api_key=%s"
CATCHUP_URL = "http://tvheute.mixd.tv/videos-broadcasted/%s/since/5/days/?api_key=%s&format=json"
API_KEY = "7bfec152-9f58-bcff-1b68-6aafb8bce621"

BROADCASTER_ID_TO_NAME = {
    "SAT": "Sat1",
    "RTS": "SUPER RTL",
    "ARD": "ARDApi",
    "SIX": "Sixx",
    "OR3": "ORF3",
    "OR1": "ORFEins",
    "RT2": "RTL2",
    "RTL": "RTL",
    "STA": "ServusTv",
    "OR2": "ORF2",
    "K1": "Kabel Eins",
    "ATV": "ATV",
    "P7": "Pro7",
    "3SA": "3SAApi",
    "ZDF": "ZDFApi",
    "OSP": "ORFSport",
    "ART": "arte.TV",
    "VOX": "VOX",
    "PU4": "Puls4",
}

class MatchingChecker:
    def __init__(self):
        print "Initializing Matching Checker",

    def start_check(self, broadcaster_id):
        print "Starting check for broadcaster " + broadcaster_id
        broadcaster_name = BROADCASTER_ID_TO_NAME[broadcaster_id]
        sources_json = json.loads(urllib.urlopen(SOURCES_URL % API_KEY).read())
        for item in sources_json['msg']:
            if item['name'] == broadcaster_name:
                broadcaster_entity_id = item['entityId']
        print "-> Broadcaster entity ID: " + broadcaster_entity_id
        self.start_catchup_check(broadcaster_entity_id)
        self.start_epg_check(broadcaster_id)

    def start_catchup_check(self, broadcaster_entity_id):
        checkup_json = json.loads(urllib.urlopen(CATCHUP_URL % (broadcaster_entity_id, API_KEY)).read())
        videos = checkup_json['msg']['data']
        matched_items = 0
        for item in videos:
            if item['epgIds']:
                matched_items += 1
        print "-> Catchup data found: %d EPG entries in %d Catchup Vidoes" % (matched_items, len(videos))

    def start_epg_check(self, broadcaster_id):
        now = datetime.datetime.now()
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)

        url = EPG_URL % (broadcaster_id, seven_days_ago.strftime("%s"), now.strftime("%s"), API_KEY)
        # print "-> reading from " +  url
        epg_json = json.loads(urllib.urlopen(url).read())

        videos = epg_json['msg']['data']
        matched_items = 0
        for item in videos:
            if item['onlineVideos']:
                matched_items += 1
        print "-> EPG data found: %d Catchup entries in %d EPG Entries" % (matched_items, len(videos))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--broadcaster', default="all", help='BroadcasterId to be checked')
    # parser.add_argument('--restore', action='store_true', default=False, help='Restore from last Backup')
    args = parser.parse_args()
    matching_checker = MatchingChecker()
    matching_checker.start_check(args.broadcaster)
