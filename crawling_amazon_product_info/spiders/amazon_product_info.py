# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class AmazonProductInfoSpider(scrapy.Spider):
    name = "amazon_product_info"
    allowed_domains = ["amazon.co.jp"]
    start_urls = (
        'http://www.amazon.co.jp/s/keywords=%E9%87%91%E5%B1%9E%E5%B7%A5%E4%BD%9C%E6%8A%80%E8%A1%93',
    )

    def parse(self, response):
        soup = BeautifulSoup(response.body)

        # 次のページへのリンクが記載された要素を取得
        next_page = soup.find('a', {'id': 'pagnNextLink'})

        if 'href' not in next_page.attrs:
            # 次のページが見つからなかった場合は終了
            yield

        # コンテンツの情報を取得
        products_ul = soup.find('ul', {'id': 's-results-list-atf'})
        for product_li in products_ul.findAll('li'):
            if product_li.get('id') != None:
                product_asin = product_li.get('data-asin')
                print product_asin

                product_title = product_li.find('h2', {'class': 'a-size-base a-color-null s-inline s-access-title a-text-normal'})
                print product_title.text

                print '--------------------------'

        # 次のページヘのリンクを組み立てる
        base_url = 'http://www.amazon.co.jp/'
        next_path = next_page['href']
        next_url = '{base_url}{next_path}'.format(base_url=base_url, next_path=next_path)
        print next_url

        # scrapy.Request を返すと次にクロールするページの指定になる
        next_crawl_page = scrapy.Request(next_url)
        yield next_crawl_page
