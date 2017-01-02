
import json

import scrapy
from scrapy.http import Request

from ScholarBar.items import ScholarItem

class IEEESpider(scrapy.Spider):
    name = 'ieee'

    def start_requests(self):
        return [Request(
            url = 'http://ieeexplore.ieee.org/rest/search',
            method = 'POST',
            headers = {'Content-Type': 'application/json'},
            body = '{"queryText":"audio generation", "newsearch":"true", "rowsPerPage":"2"}'
        )]

    def item_selector(self):
        return 'div.article-list div.pure-u-22-24'

    def ieee_text_escape(self, text):
        return text.replace('[::', '').replace('::]', '')

    def parse(self, response):
        json_response = json.loads(response.body)
        for record in json_response['records']:
            item = ScholarItem()
            item['title'] = self.ieee_text_escape(record['title'])
            item['year'] = record['publicationYear']
            item['publisher'] = record['publisher']
            item['authors'] = [i['preferredName'] for i in record['authors']]
            item['affiliation'] = None
            item['citation_count'] = record['citationCount']
            item['link'] = response.urljoin(record['documentLink'])
            item['download_link'] = response.urljoin(record['pdfLink'])
            yield item
