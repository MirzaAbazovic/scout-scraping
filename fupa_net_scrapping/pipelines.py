# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from cloudant import Cloudant
from scrapy.exceptions import DropItem

class FupaNetScrappingPipeline(object):
    def process_item(self, item, spider):
        cloudant_user = os.environ["CLOUDANT_USER"]
        cloudant_pass = os.environ["CLOUDANT_PASS"]
        client = Cloudant(cloudant_user, cloudant_pass, account=cloudant_user)
        client.connect()
        session = client.session()
        scout_database = client['scout']
        data = {
            'type' : 'player',
            'clubImageUrl': item['clubImageUrl'],
            'clubName': item['clubName'],
            'firstName': item['firstName'],
            'lastName': item['lastName'],
            'playerId': item['playerId'],
            'playerUrl': item['playerUrl'],
            'playerUrlShort': item['playerUrlShort']
        }
        my_database = client['scout']
        my_document = my_database.create_document(data)
        if my_document.exists():
            print 'Created document.'
            return item
        else:
            raise DropItem("Failed to post item with id  %s." % item['playerId'])
            client.disconnect()