# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class AmazonProductIdSpider(scrapy.Spider):
    name = "amazon_product_id"
    allowed_domains = ["www.amazon.co.jp"]
    start_urls = (
        'http://www.www.amazon.co.jp/',
    )

    def parse(self, response):
        pass
