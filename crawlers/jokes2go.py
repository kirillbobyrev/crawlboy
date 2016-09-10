# -*- coding: utf-8 -*-
'''Crawl http://www.jokes2go.net jokes.

$ scrapy runspider unijokes.py --output-format=jsonlines \ 
                               -o ../data/unijokes.jsonlines
'''

import scrapy


class MyEnglishPagesSpider(scrapy.Spider):
    name = 'jokes2go.net'

    start_urls = ['http://www.jokes2go.net/joke/{}'.format(joke_id) for joke_id
                  in range(1, 22000)]

    def parse(self, response):
        jk = response.xpath('//div[@class="joke"]/p/text()')
        yield {
            'text': '\n'.join([l.strip(' \n\r') for l in jk.extract()
                               if l.strip(' \n\r')]),
        }
