# -*- coding: utf-8 -*-

# Scrapy settings for ScholarBar project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

####################### ScholarBar Settings #############################

import re
from scrapy.http import Request

from ScholarBar.utils import html_text

KEYWORDS = ['audio generation']

MAX_CRAWL_COUNT_EACH_SPIDER = 6

CRAWLERS = {
    # json response example
    'ieee': {
        'response_type': 'json',
        'page_size': 10,
        'start_page_index': 1,
        'request_generator': lambda keyword, page_size, page_index: Request(
            url = 'http://ieeexplore.ieee.org/rest/search',
            method = 'POST',
            headers = {'Content-Type': 'application/json'},
            body = '{{"queryText": "{0}", "newsearch":"true", "rowsPerPage":"{1}", "pageNumber":"{2}"}}'.format(keyword, page_size, page_index)
        ),
        'scholar_item': {
            'selector': '.records > div',
            'title': '.title',
            'year': '.publicationYear',
            'publisher': '.publisher',
            'authors': '.authors > div > .preferredName',
            'affiliation': None,
            'citation_count': '.citationCount',
            'link': '.documentLink',
            'download_link': '.pdfLink',
        }
    },

    # html response example
    'bing': {
        'response_type': 'html',
        'page_size': 10,
        'start_page_index': 0,
        'request_generator': lambda keyword, page_size, page_index: Request(
            url = 'http://cn.bing.com/academic/search?q={0}&first={1}'.format(re.sub(r'\s+', '+', keyword), page_size*page_index + 1)
        ),
        'scholar_item': {
            'selector': '#b_results > li.aca_algo',
            'title': 'h2',
            'year': {
                'selector': '.caption_venue',
                'post_convertor': lambda x: re.findall(r'\d{4}', html_text(x))[0],
            },
            'publisher': '.caption_venue > a:nth-of-type(1)',
            'authors': {
                'selector': '.caption_author',
                'post_convertor': lambda s: list(map(lambda x: x.strip(), html_text(s).split(u'\xb7')))
            },
            'affiliation': None,
            'citation_count': '.caption_venue > a:nth-of-type(2)',
            'link': {
                'selector': 'h2/a/@href',
                'is_css': False,
            },
            'download_link': None,
        }
    }
}

####################### System Settings #############################

BOT_NAME = 'ScholarBar'

SPIDER_MODULES = ['ScholarBar.spiders']
NEWSPIDER_MODULE = 'ScholarBar.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ScholarBar (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ScholarBar.middlewares.ScholarbarSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ScholarBar.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'ScholarBar.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
