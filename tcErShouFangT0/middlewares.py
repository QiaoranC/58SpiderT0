# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.conf import settings
import random
from redis import Redis
import logging


logger = logging.getLogger()

class Tcershoufangt0SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def process_request(self, request, spider):
    # 讯代理 =============================================================================================
        import sys
        import time
        import hashlib
        # import requests
        # import grequests
        from lxml import etree

        _version = sys.version_info

        is_python3 = (_version[0] == 3)

        orderno = "ZF201792160911aQXzH"
        secret = "b468bd39d26c46b5aa77d3cef4d9204d"

        ip = "forward.xdaili.cn"
        port = "80"

        ip_port = ip + ":" + port

        timestamp = str(int(time.time()))                # 计算时间戳
        string = ""
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

        if is_python3:
            string = string.encode()

        md5_string = hashlib.md5(string).hexdigest()                 # 计算sign
        sign = md5_string.upper()                              # 转换成大写
        print(sign)
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        #
        print(auth)
        # proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
        # headers = {"Proxy-Authorization": auth}

        request.meta["proxy"] = "forward.xdaili.cn:80"
        request.headers["Proxy-Authorization"] = auth
        # ===================================================================================================
        ua  = random.choice(settings.get('USER_AGENT_LIST'))

        if ua:
            # logger.info(ua)
            request.headers.setdefault('User-Agent', ua)
        else:
            logger.info('获取随机ua失败,使用Scrapy默认代理')
    
    
    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls()
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s
    # 
    # def process_spider_input(self, response, spider):
    #     # Called for each response that goes through the spider
    #     # middleware and into the spider.
    # 
    #     # Should return None or raise an exception.
    #     return None
    # 
    # def process_spider_output(self, response, result, spider):
    #     # Called with the results returned from the Spider, after
    #     # it has processed the response.
    # 
    #     # Must return an iterable of Request, dict or Item objects.
    #     for i in result:
    #         yield i
    # 
    # def process_spider_exception(self, response, exception, spider):
    #     # Called when a spider or process_spider_input() method
    #     # (from other spider middleware) raises an exception.
    # 
    #     # Should return either None or an iterable of Response, dict
    #     # or Item objects.
    #     pass
    # 
    # def process_start_requests(self, start_requests, spider):
    #     # Called with the start requests of the spider, and works
    #     # similarly to the process_spider_output() method, except
    #     # that it doesn’t have a response associated.
    # 
    #     # Must return only requests (not items).
    #     for r in start_requests:
    #         yield r
    # 
    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)
