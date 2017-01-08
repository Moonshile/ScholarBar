
import math
import json
from abc import ABCMeta

import scrapy
from scrapy.http import Request

from ScholarBar.items import ScholarItem
from ScholarBar.settings import KEYWORDS,\
    MAX_CRAWL_COUNT_EACH_SPIDER as maxCount,\
    CRAWLERS

from ScholarBar.utils import dict2html, html_text

class AbstractSpider(scrapy.Spider):
    __metaclass__ = ABCMeta

    def start_requests(self):
        req_gen = self.conf['request_generator']
        page_size = self.conf['page_size']
        start_page_index = self.conf['start_page_index']
        max_page_index = int(math.ceil(maxCount/float(page_size))) + start_page_index
        page_indexes = range(start_page_index, max_page_index)
        return list(
            reduce(lambda res, keyword:
                res + map(lambda i: req_gen(keyword, page_size, i), page_indexes),
                KEYWORDS, []
            )
        )

    def parse(self, response):
        if self.conf['response_type'] == 'json':
            html_gen = dict2html(json.loads(response.body))
            html_str = u'<!DOCTYPE html><html><body>\n{0}</body></html>'.format(html_gen)
            response = response.replace(body=html_str)
        item_info = self.conf['scholar_item']
        items = response.css(item_info['selector'])
        for record in items:
            item = ScholarItem()
            try:
                for k, v in item_info.items():
                    if k == 'selector' or not v:
                        continue

                    post_converter = html_text
                    extractor = record.css
                    if isinstance(v, dict):
                        post_converter = v.get('post_convertor', post_converter)
                        extractor = record.css if v.get('is_css', True) else record.xpath
                        v = v['selector']

                    values = extractor(v).extract()
                    item[k] = post_converter(values[0]) if len(values) == 1 else list(map(lambda x: post_converter(x), values))

                    if k in {'link', 'download_link'}:
                        item[k] = response.urljoin(item[k])
            except Exception, e:
                print(e)
            yield item

class IEEESpider(AbstractSpider):
    name = 'ieee'

    def start_requests(self):
        """
        IEEE require cookies, so must override start_requests to fetch the cookies
        After that, post_requests as a callback, will perform what start_requests performed
        """
        return [Request(url='http://ieeexplore.ieee.org/robots.txt', callback=self.post_requests)]

    def post_requests(self, response):
        return super(IEEESpider, self).start_requests()

    def __init__(self):
        super(IEEESpider, self).__init__()
        self.conf = CRAWLERS[IEEESpider.name]

class BingScholarSpider(AbstractSpider):
    name = 'bing'

    def __init__(self):
        super(BingScholarSpider, self).__init__()
        self.conf = CRAWLERS[BingScholarSpider.name]
