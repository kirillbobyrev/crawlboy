# -*- coding: utf-8 -*-
'''Crawl http://unijokes.com jokes.

$ scrapy runspider unijokes.py --output-format=jsonlines \ 
                               -o ../data/unijokes.jsonlines
'''

import scrapy


class UnijokesSpider(scrapy.Spider):
    name = 'unijokes.com'

    start_urls = ['http://unijokes.com/{}/'.format(page)
                  for page in range(1, 1178)]

    def parse(self, response):
        for div in response.xpath('//div[@class="joke"]'):
            jk = div.xpath('text()').extract_first().replace('\r', '')
            yield {
                'text': jk
            }
