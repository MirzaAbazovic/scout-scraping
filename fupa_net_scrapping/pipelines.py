# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
from cloudant import Cloudant
from scrapy.exceptions import DropItem
import mimetypes
import base64

class FupaNetScrappingPipeline(object):
    
    def __init__(self):
        mimetypes.init()
        cloudant_user = os.environ["CLOUDANT_USER"]
        cloudant_pass = os.environ["CLOUDANT_PASS"]
        client = Cloudant(cloudant_user, cloudant_pass, account=cloudant_user)
        client.connect()
        session = client.session()
        self.database = client['scout']
        self.client = client
    
    def __del__(self):
        self.client.disconnect()
        #print ('disconect')
    
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
            'file_urls': item['file_urls'],
            'files': item['files']
        }
        #return item
        # data['_attachments'] = {}
        # attachments = []
        # #data['_attachments'] = {file_name : {'data': uploaded_file_content}}
        # for fileItem in item['files']:
        #     f = open('C:/Users/mir/projects/fupa_net_scrapping/images/'+fileItem['path'],'r+')
        #     #f = open('photo.jpg', 'r+')
        #     jpgdata = f.read()
        #     encoded = base64.b64encode(jpgdata)
        #     f.close()
        #     name = fileItem['url']
        #     #m_t = mimetypes.guess_type(name)
        #     #print(m_t)
        #     print('put attach')
        #     attachments.append(({name:{'data':encoded}}))
        #     #resp = my_document.put_attachment( attachment = name, data = jpgdata , content_type = 'image/jpeg')
        #     print attachments
        # data['_attachments'] = attachments
        my_document = self.database.create_document(data)
        if my_document.exists():
             return item
        else:
             raise DropItem("Failed to post item with id  %s." % item['playerId'])