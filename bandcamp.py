import requests
import json
import random
from database import *

import os
import requests
import sys
import psycopg2
from flask import request
from discord_webhook import DiscordWebhook, DiscordEmbed
import random

try:
    import config
except:
    pass

import random
from discord_webhook import DiscordWebhook, DiscordEmbed

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = config.DATABASE_URL
try:
    WEBHOOK = os.environ['WEBHOOK']
except:
    WEBHOOK = config.WEBHOOK
try:
    TAGS = os.environ['TAGS'].split(",")
except:
    TAGS = config.TAGS

connection = psycopg2.connect(DATABASE_URL, sslmode='require')
db = Database(connection=connection)

cookies = {
    'client_id': 'ABD11130490FB8BAB0A36F719D412B26AB4D442DDC572947E0CEBC449B5F2AF5',
    'BACKENDID3': 'flexocentral-k4tc-5',
    'BACKENDID': 'flexo1central-msnj-6',
    'session': '1%09t%3A1676836927%09r%3A%5B%22436538439s0g0x1676837105%22%2C%22nilZ0f0x1676836927%22%2C%2210394G0a925196547x1676788772%22%5D%09bp%3A1',
}

headers = {
    'authority': 'bandcamp.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://bandcamp.com',
    'referer': 'https://bandcamp.com/tag/lofi-hiphop?from=search&search_item_id=2&search_item_type=%40&search_match_part=%3F&search_page_id=2440068440&search_page_no=1&search_rank=1&search_sig=b6fd221a40566ee1960908a52cf7a385&tab=all_releases&s=date',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


collection = []
collection_items = []


all = db.getBandcamp()
for a in all:
    collection.append("{} - {}".format(a[0], a[1]))

for t in TAGS:
    page = 1

    while True:
        json_data = {
            'filters': {
                "format": "all",
                'location': 0,
                'sort': 'date',
                'tags': [
                    t,
                ],
            },
            'page': page,
        }

        response = requests.post('https://bandcamp.com/api/hub/2/dig_deeper', cookies=cookies, headers=headers, json=json_data)
        json_data = json.loads(response.text)
        #print("NUM OF ALBUMS: {}".format(len(json_data["items"])))
        for item in json_data["items"]:
            album_title = item["title"]
            artist = item["artist"]
            strr = "{} - {}".format(artist, album_title)
            if strr not in collection:
                collection.append(strr)
                collection_items.append([item["artist"], item["title"], item["tralbum_url"], item["tralbum_id"]])
                db.saveBandcamp(item["artist"], item["title"], item["tralbum_url"], item["tralbum_id"], "no")
                print("NEW ONE SAVED!")
            else:
                #print("{} already in collection!!!".format(strr))
                pass
        #print("LEN OF COLLECTION: {}".format(len(collection)))
        if len(json_data["items"]) == 0:
            break
        page += 1

all = db.getBandcamp()
webhook = DiscordWebhook(url=WEBHOOK, content="Scraped new Bandcamp content. Total albums now: {}".format(len(all)))
response = webhook.execute()