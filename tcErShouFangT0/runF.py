from scrapy.cmdline import execute
# from redis import Redis
import sys
import os
import redis
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# connection_object = redis.Redis(host='106.75.166.130', port=6379, db=0, password='v5e7r8o4n4i9c0a9')

# r = redis.Redis()
r = redis.StrictRedis(host='106.75.166.130', port=6379, db=0, password='v5e7r8o4n4i9c0a9')
r.delete('tcErShouFang:Start_URL')
r.lpush('tcErShouFang:Start_URL',"http://la.58.com")
execute(["scrapy","crawl","tcErShouFangFixedURLs"])
# scrapy crawl tcErShouFangFixedURLs tcErShouFanglist