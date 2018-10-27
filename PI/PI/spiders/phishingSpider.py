# -*- coding: utf-8 -*-
import scrapy
# from scrapy_splash import SplashFormReques


class PhishingSpider(scrapy.Spider):
    name = 'phishingSpider'
    
    def __init__(self,domain='',**kwargs):
        self.start_urls = [domain]
    
    def start_requests(self):
       allowed_domains = ['deloitte.com']
       
       for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'phish-site.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
