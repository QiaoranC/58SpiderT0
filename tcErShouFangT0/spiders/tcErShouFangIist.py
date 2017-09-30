# -*- coding: utf-8 -*-
import scrapy
import re
# from redis import Redis
import redis
from scrapy_redis.spiders import RedisSpider

# error系列
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from scrapy.loader import ItemLoader
from scrapy.http import Request
from urllib import parse
import logging

from tcErShouFangT0.items import Tcershoufangt0Item

#log文件==========================================================================
import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='logList.txt',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.WARNING
)
#===============================================================================

logger = logging.getLogger()
r = redis.StrictRedis(host='106.75.166.130', port=6379, db=0, password='v5e7r8o4n4i9c0a9')

class TcershoufangSpider(RedisSpider):
    name = 'tcErShouFanglist'
    redis_key = '58House:FixedPosition'

    def parse(self, response):
        Rurl = str(response.url)
        next_url = response.xpath('//*[contains(@class,"next")]//@href').extract_first()
        
        if re.search(r'chuzu',Rurl):
            urls = response.xpath('//ul[@class="listUl"]/li[@logr][@sortid]/div[@class="img_list"]//@href').extract()
            if urls:
                for url in urls:
                    r.rpush('58House:All', url)
                if next_url:
                    yield Request(next_url,callback=self.parse, errback=self.errback_httpbin) 
            else:
                logger.info("V's No list available in  %s" % Rurl)
        elif re.search(r'qiuzu',Rurl): 
            urls = response.xpath('//table[@class="tblist"]//tr[@logr]//a[@data-addtype]//@href').extract()
            if urls:
                for url in urls:
                    r.rpush('58House:All', url)
                if next_url:
                    yield Request(next_url,callback=self.parse, errback=self.errback_httpbin) 
            else:
                logger.info("V's No list available in  %s" % Rurl)
        elif re.search(r'duanzu',Rurl): 
            urls = response.xpath('//table[@class="tbimg ttborder"]//tr[@logr]//td[@class="img"]//@href').extract()
            if urls:
                for url in urls:
                    r.rpush('58House:All', url)
                if next_url:
                    yield Request(next_url,callback=self.parse, errback=self.errback_httpbin) 
            else:
                logger.info("V's No list available in  %s" % Rurl)
        else:
            urlsNoS = response.xpath('//ul[@class="house-list-wrap"]/li[@logr]/div[@class="list-info warehouse"]//@href').extract()
            urlsS = response.xpath('//ul[@class="house-list-wrap"]/li[@logr]//h2[@class="title"]//@href').extract()
            if urlsNoS:
                for urlNoS in urlsNoS:
                    r.rpush('58House:All', urlNoS)
                if next_url:
                    yield Request(next_url, callback=self.parse, errback=self.errback_httpbin) 
            elif urlsS:
                for urlS in urlsS:
                    r.rpush('58House:All', urlS)
                if next_url:
                    yield Request(next_url, callback=self.parse, errback=self.errback_httpbin)
            elif urlsNoS and urlsS:
                for urlNoS in urlsNoS:
                    r.rpush('58House:All', urlNoS)
                    logger.info("V's both have urlsNoS and urlsS in %s" % Rurl)
                if next_url:
                    yield Request(next_url, callback=self.parse, errback=self.errback_httpbin) 
            else:
                logger.info("V's No list available in  %s" % Rurl)


#Error===================================================================================================================
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("V's Occur HttpError on %s", response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error("V's Occur DNSLookupError on %s", request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("V's Occur TimeoutError on %s", request.url)
#========================================================================================================================
