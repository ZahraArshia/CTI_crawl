import scrapy
import re

regex = re.compile(r"<[^>]+>")

def remove_html(string):
    return regex.sub('', string)

class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.thehackernews.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://thehackernews.com', 
            callback=self.parse, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            },
            meta = {
                'first': True
            }
            )

    def parse(self, response):
        links = response.xpath('//a[contains(@class, "story-link")]/@href')
        for link in links:
            yield response.follow(
                url = link.get(),
                callback = self.thred,
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                },
                meta={
                    'link': link.get(),
                    'first': True
                }
            )

            next_page = response.xpath('(//a[contains(@class, "blog-pager-older-link-mobile")])/@href').get()
            yield response.follow(
                url = next_page,
                callback = self.parse,
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                },
                meta={
                    'first': False
                }
            )

    def thred(self, response):
        articles = response.xpath('//div[contains(@class, "articlebody")]')
        for article in articles:
            yield{
                'article': remove_html(article.get()),
                'link': response.request.meta['link']
            }

