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
    files = scrapy.Field()
    file_urls = scrapy.Field()
    # playerImage = scrapy.Field()
        

class PlayerSpider(scrapy.Spider):
    name = 'players_list'
    allowed_domains = ['www.fupa.net']
    # start_urls = ["http://www.fupa.net/liga/u19_bundesliga_sued-suedwest-31423/statistik.html?order=einsaetze&seite=1"]
    start_urls = ["http://www.fupa.net/liga/u19_bundesliga_sued-suedwest-31423/statistik.html?order=einsaetze&seite=1"]
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
                        file_urls = [club_image_url])
                    #print 'GOTO '+player_url
                    #item['file_urls'] = club_image_url
                    request = scrapy.Request(player_url, callback=self.parse_details)
                    request.meta['item'] = item
                    yield request # item #PlayerItem( position=item['position'], firstName=first_name, lastName=last_name, playerId = player_id, playerUrl = player_url, playerUrlShort = player_url_short, clubName=club_name, clubImageUrl = club_image_url)
                next_page = response.css('a.forward_button').xpath('@href').extract_first()
                if next_page:
                    print(next_page)
                    #yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    
    # def validate_date(self, date_text):
    #     try:
    #         if date_text != datetime.strptime(date_text, "%d.%m.%Y").strftime('%d.%m.%Y'):
    #             raise ValueError
    #             return True
    #     except ValueError:
    #         return False
    
    def parse_details(self, response):
        item = response.meta['item']
        item['position']  = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[1]/td[2]/b/text()').extract_first()
        dob = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[2]/td[2]/text()').extract_first()
        # if self.validate_date(dob[:10]):
        #     item['dob']  = dob[:10]
        if len(dob) > 9:
            item['dob']  = dob[:10]
        item['nationality'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[3]/td[2]/img/@title').extract()
        item['nationalityFlagUrl'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[3]/td[2]/img/@src').extract()
        item['leauge'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[2]/table/tr[8]/td[2]/a[2]/text()').extract()
        item['playerImageUrl'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[1]/img/@src').extract()
        item['file_urls'].insert(response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[1]/img/@src').extract())
        #item['file_urls'] = response.xpath('/html/body/div[1]/div[2]/div[1]/table[1]/tr/td[1]/img/@src').extract()
        print item['file_urls']
        yield item
    