# spieler_statistik_list_spider.py

import re
import scrapy
#from dateutil.parser import parse
#from datetime import datetime

class PlayerItem(scrapy.Item):
    firstName = scrapy.Field()
    lastName = scrapy.Field()
    playerId = scrapy.Field()
    playerUrl = scrapy.Field()
    playerUrlShort = scrapy.Field()
    clubName = scrapy.Field()
    clubImageUrl = scrapy.Field()
    position = scrapy.Field()
    dob = scrapy.Field() 
    nationality = scrapy.Field()
    nationalityFlagUrl = scrapy.Field()
    leauge = scrapy.Field()
    playerImageUrl = scrapy.Field()
    images = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
        

class PlayerSpider(scrapy.Spider):
    name = 'players_list'
    allowed_domains = ['www.fupa.net']
    #start_urls = ["http://www.fupa.net/liga/u19_bundesliga_sued-suedwest-31423/statistik.html?order=einsaetze&seite=1"]
    start_urls = [
        "http://www.fupa.net/liga/u19_bundesliga_sued-suedwest-31423/statistik.html?order=einsaetze&seite=1",
        "http://www.fupa.net/liga/u17-bundesliga-sued-suedwest-34826/statistik.html?order=einsaetze&seite=1",
        "http://www.fupa.net/liga/a-junioren-bundesliga-west-31480/statistik.html?order=einsaetze&seite=1",
        "http://www.fupa.net/liga/b-junioren-bundesliga-west-31703/statistik.html?order=einsaetze&seite=1",
        "http://www.fupa.net/liga/u19-bundesliga-nord-nordost-34255/statistik.html?order=einsaetze&seite=1"]

    def parse(self, response):
        
        TABLE_XPATH = '//*[@id="ip_content_wrapper"]/div[2]/div[2]/table'
        table = response.xpath(TABLE_XPATH)
        for row in table.xpath('tr'):
            NAME_XPATH = 'td/a/span//text()'
            name = row.xpath(NAME_XPATH).extract()
            if len(name) == 2:
                first_name = name[0]
                last_name = name[1]
                PLAYER_ID_XPATH = 'td/a/@id'
                player_id = row.xpath(PLAYER_ID_XPATH).extract()[0].split("_")[1]
                PLAYER_URL_SUFIX = "http://www.fupa.net/fupa/api.php?p=spieler_effectif_get_kurzinfo&eff_id="
                player_url_short =  PLAYER_URL_SUFIX + player_id
                CLUB_NAME_XPATH = 'td/img/@alt'
                club_name = row.xpath(CLUB_NAME_XPATH).extract()[0]
                CLUB_IMAGE_XPATH = 'td/img/@src'
                club_image_url = row.xpath(CLUB_IMAGE_XPATH).extract()[0]
                PLAYER_URL_XPATH = 'td/a/@href'
                player_url = row.xpath(PLAYER_URL_XPATH).extract_first()
                if player_url:
                    item = PlayerItem(
                        firstName=first_name,
                        lastName=last_name,
                        playerId = player_id,
                        playerUrl = player_url,
                        playerUrlShort = player_url_short,
                        clubName=club_name,
                        clubImageUrl = club_image_url,
                        )
                    item['file_urls'] = []
                    if club_image_url is not None:
                        item['file_urls'].append(club_image_url)
                    request = scrapy.Request(player_url, callback=self.parse_details)
                    request.meta['item'] = item
                    yield request 
                next_page = response.css('a.forward_button').xpath('@href').extract_first()
                if next_page:
                    #print(next_page)
                    yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    
    def parse_details(self, response):
        item = response.meta['item']
        item['position']  = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[1]/td[2]/b/text()').extract_first()
        dob = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[2]/td[2]/text()').extract_first()
        #if len(dob) > 9:
        #    item['dob']  = dob[:10]
        item['dob']  = dob
        item['nationality'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[3]/td[2]/img/@title').extract_first()
        
        item['nationalityFlagUrl'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[3]/td[2]/img/@src').extract_first()
        if item['nationalityFlagUrl'] is not None:
            item['file_urls'].append(item['nationalityFlagUrl'])
        
        item['leauge'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[8]/td[2]/a[2]/text()').extract_first()

        item['playerImageUrl'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[1]/img/@src').extract_first()
        if item['playerImageUrl'] is not None:
            item['file_urls'].append(item['playerImageUrl'])
        
        #print item['file_urls']
        yield item
    