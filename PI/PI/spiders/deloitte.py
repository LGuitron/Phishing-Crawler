# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

# TODO: Publish to firebase and call from flask API
class DeloitteSpider(scrapy.Spider):
    name = 'deloitte'
    
    def start_requests(self):
       start_urls = ['https://www2.deloitte.com/mx/es.html', 'https://www2.deloitte.com/mx/es/pages/energy-and-resources/articles/la-paradoja-de-la-industria-4-0.html']
       for url in start_urls:
            yield SplashRequest(
                url=url, 
                callback=self.parse
            )
     


    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = 'page-%s.html' % page
        yield response
