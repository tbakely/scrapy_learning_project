import scrapy
from scrapy.loader import ItemLoader
from nflspider.items import NflspiderItem


class NflcrawlSpider(scrapy.Spider):
    name = 'nflcrawl'
    allowed_domains = ['nfl.com']
    start_urls = ['http://nfl.com/stats/player-stats']
    custom_settings = {'FEED_EXPORT_FIELDS': ['PLAYERS', 'PASS_YDS', 'YDS_ATT', 'ATT', 'CMP', 'CMP_PERC', 'TD',
                                              'INT', 'PASS_RATING', 'FIRST_DOWN', 'FIRST_DOWN_PERC', 'TWENTY_PLUS',
                                              'FORTY_PLUS', 'LONG', 'SACK', 'SACK_YARDS']}

    def parse(self, response):
        for p in response.xpath('//table/tbody//tr'):
            l = ItemLoader(item=NflspiderItem(), selector=p)
            l.add_xpath('PLAYERS', './/a[@class="d3-o-player-fullname nfl-o-cta--link"]')
            l.add_xpath('PASS_YDS', './td[2]')
            l.add_xpath('YDS_ATT', './td[3]')
            l.add_xpath('ATT', './td[4]')
            l.add_xpath('CMP', './td[5]')
            l.add_xpath('CMP_PERC', './td[6]')
            l.add_xpath('TD', './td[7]')
            l.add_xpath('INT', './td[8]')
            l.add_xpath('PASS_RATING', './td[9]')
            l.add_xpath('FIRST_DOWN', './td[10]')
            l.add_xpath('FIRST_DOWN_PERC', './td[11]')
            l.add_xpath('TWENTY_PLUS', './td[12]')
            l.add_xpath('FORTY_PLUS', './td[13]')
            l.add_xpath('LONG', './td[14]')
            l.add_xpath('SACK', './td[15]')
            l.add_xpath('SACK_YARDS', './td[16]')

            yield l.load_item()

        next_page = response.xpath("//a[@class='nfl-o-table-pagination__next']/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
