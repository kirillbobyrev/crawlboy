# -*- coding: utf-8 -*-
'''Crawl http://www.zakonrf.info/ Russian laws.

$ scrapy runspider zakonrf.py --output-format=jsonlines \ 
                               -o ../../data/laws/zakonrf.jsonlines
'''

import scrapy
from urllib.parse import urljoin


class ZakonrfSpider(scrapy.Spider):
    name = 'zakonrf.info'

    start_urls = ['http://www.zakonrf.info/content/view/zakony/',
                  'http://www.zakonrf.info/content/view/kodeksy/']

    def parse(self, response):
        for lawbook in response.xpath('//li[@class="law-row"]/a/@href'):
            yield scrapy.Request(urljoin(response.url, lawbook.extract()),
                                 callback=self.parse_lawbook)

    def parse_lawbook(self, response):
        for lawarticle in response.xpath('//li[@class="st l2"]/a/@href'):
            yield scrapy.Request(urljoin(response.url, lawarticle.extract()),
                                 callback=self.parse_lawarticle)

    def parse_lawarticle(self, response):
        article_sel = response.xpath('//div[@class="st-section"]')
        title = article_sel.xpath('header/h2/text()').extract_first()
        pathway = article_sel.xpath('header/div[@class="st-pathway"]'
                                    '/a/text()').extract()
        text = '\n'.join(article_sel.xpath('div[@class="st-body"]'
                                           '/p/text()').extract())
        yield {
            'title': title,
            'pathway': pathway,
            'text': text,
        }
