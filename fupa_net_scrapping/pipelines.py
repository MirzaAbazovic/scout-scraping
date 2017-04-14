# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from cloudant import Cloudant
from scrapy.exceptions import DropItem

class FupaNetScrappingPipeline(object):
    
    def __init__(self):
        cloudant_user = os.environ["CLOUDANT_USER"]
        cloudant_pass = os.environ["CLOUDANT_PASS"]
        client = Cloudant(cloudant_user, cloudant_pass, account=cloudant_user)
        client.connect()
        session = client.session()
        self.database = client['scout']
        self.client = client
    
    def __del__(self):
        self.client.disconnect()
        print ('disconect')
    
    def process_item(self, item, spider):
        id = item['firstName']+':'+item['lastName']+':'+item['playerId']
        data = {
            #'_id' : id,
            'type' : 'player',
            'clubImageUrl': item['clubImageUrl'],
            'clubName': item['clubName'],
            'firstName': item['firstName'],
            'lastName': item['lastName'],
            'playerId': item['playerId'],
            'playerUrl': item['playerUrl'],
            'playerUrlShort': item['playerUrlShort'],
            'position': item['position'],
            'dob': item['dob'],
            'nationality' :item['nationality'],
            'nationalityFlagUrl' :item['nationalityFlagUrl'],
            'leauge' :item['leauge'],
            'playerImageUrl': item['playerImageUrl'],
            'file_urls': item['file_urls']
        }
        return item
        # my_document = self.database.create_document(data)
        # if my_document.exists():
        #     print 'Document created'
        #     return item
        # else:
        #     raise DropItem("Failed to post item with id  %s." % item['playerId'])
        #def get_media_requests(self, item, info):
        #    yield scrapy.Request(item['file_urls'])