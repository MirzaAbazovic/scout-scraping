# spieler_statistik_list_spider.py

import scrapy
import re
# A. Define the data to be scraped
class PlayerItem(scrapy.Item):
    firstName = scrapy.Field()
    lastName = scrapy.Field()
    playerId = scrapy.Field()
    playerUrl = scrapy.Field()
    playerUrlShort = scrapy.Field()
    clubName = scrapy.Field()
    clubImageUrl = scrapy.Field()

# B Create a named spider
class PlayerSpider(scrapy.Spider):
    """ Scrapes the country and link text of the Nobel-winners. """

    name = 'players_list'
    allowed_domains = ['www.fupa.net']
    start_urls = ["http://www.fupa.net/liga/u19_bundesliga_sued-suedwest-31423/statistik.html?order=einsaetze&seite=1","http://www.fupa.net/liga/u19_bundesliga_sued-suedwest-31423/statistik.html?order=einsaetze&seite=2"]
    # C A parse method to deal with the HTTP response
    def parse(self, response):
        table = response.xpath('//*[@id="ip_content_wrapper"]/div[2]/div[2]/table')
        
        for row in table.xpath('tr'):
            name = row.xpath('td/a/span//text()').extract()
            if(len(name)==2):
                first_name = name[0]
                last_name =  name[1]
                player_id = row.xpath('td/a/@id').extract()[0].split("_")[1]  
                player_url_short = "http://www.fupa.net/fupa/api.php?p=spieler_effectif_get_kurzinfo&eff_id="+player_id
                player_url = row.xpath('td/a/@href').extract()[0]  
                club_name = row.xpath('td/img/@alt').extract()[0] 
                club_image_url = row.xpath('td/img/@src').extract()[0] 
                yield PlayerItem( firstName=first_name, lastName=last_name, playerId = player_id, playerUrl = player_url, playerUrlShort = player_url_short, clubName=club_name, clubImageUrl = club_image_url)

            # first_name = row.xpath('td/a/span//text()')[0].extract()
            # first_name = row.xpath('td/a/span//text()')[0].extract()
            # last_name =  row.xpath('td/a/span//text()')[1].extract()
            # yield PlayerItem(first_name=first_name,last_name=last_name)