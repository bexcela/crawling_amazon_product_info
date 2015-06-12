# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class AmazonProductIdSpider(scrapy.Spider):
    name = "amazon_product_id"
    allowed_domains = ["amazon.co.jp"]
    start_urls = (
        'http://www.amazon.co.jp/s/keywords=%E3%82%AA%E3%83%A9%E3%82%A4%E3%83%AA%E3%83%BC', # テスト用にオライリー検索結果ページを指定
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
                print product_li.get('id')
                print product_li.get('data-asin')
                print '--------------------------'

        # 次のページヘのリンクを組み立てる
        base_url = 'http://www.amazon.co.jp/'
        next_path = next_page['href']
        next_url = '{base_url}{next_path}'.format(base_url=base_url, next_path=next_path)
        print next_url

        # scrapy.Request を返すと次にクロールするページの指定になる
        next_crawl_page = scrapy.Request(next_url)
        yield next_crawl_page
