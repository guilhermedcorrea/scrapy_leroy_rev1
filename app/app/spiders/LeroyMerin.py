import scrapy


class LeroymerinSpider(scrapy.Spider):
    name = "LeroyMerin"
    allowed_domains = ["leroymerlin.com.br"]
    start_urls = ["https://leroymerlin.com.br"]

    def parse(self, response):
        pass
