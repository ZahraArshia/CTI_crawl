import scrapy


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.thehackernews.com']
    start_urls = ['http://www.thehackernews.com/']

    def parse(self, response):
        pass
