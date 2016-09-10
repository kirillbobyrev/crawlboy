# -*- coding: utf-8 -*-
'''Crawl http://www.myenglishpages.com jokes.

$ scrapy runspider myenglishpages.py --output-format=jsonlines \ 
                                     -o ../data/myenglishpages.jsonlines
'''

import scrapy


class MyEnglishPagesSpider(scrapy.Spider):
    name = 'myenglishpages.com'

    start_urls = [
        'http://www.myenglishpages.com/site_php_files'
        '/jokes.php?page={}'.format(page) for page in range(1, 50)]

    def parse(self, response):
        for div in response.xpath(
                '//div[@style="margin-left:14px; margin-right:14px; '
                'padding:6px; background-color:#FFDDFF; border:#999 '
                '1px solid;"]'):
            jk = [l.strip(' \r\n|') for l in div.xpath('text()').extract()
                  if l.strip(' \r\n|')]
            yield {
                'text': '\n'.join(jk),
            }
