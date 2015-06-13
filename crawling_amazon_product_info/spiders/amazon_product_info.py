# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup


class AmazonProductInfoSpider(scrapy.Spider):
    name = "amazon_product_info"
    allowed_domains = ["amazon.co.jp"]

    def __init__(self, *args, **kwargs):
        super(AmazonProductInfoSpider, self).__init__(*args, **kwargs)

        # Load search keywords from input file(keywords.txt)
        search_keywords = []
        with open("crawling_amazon_product_info/keywords.txt") as f:
            for line in f:
                search_keywords.append(line[:-1])

        for search_keyword in search_keywords:
            self.start_urls.append('http://www.amazon.co.jp/s/keywords=%s' % search_keyword)


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
            try:
                if product_li.get('id') != None:
                    # asin
                    product_asin = product_li.get('data-asin')
                    print product_asin

                    # title
                    product_title = product_li.find('h2', {'class': 'a-size-base a-color-null s-inline s-access-title a-text-normal'})
                    print product_title.text

                    # authors
                    authors_area = product_li.find('div', {'class': 'a-row a-spacing-mini'})
                    if authors_area != None:
                        product_authors = authors_area.findAll('span', {'class': 'a-size-small a-color-secondary'})

                        for product_author in product_authors:
                            if (len(product_author.text) != 0):
                                if not re.match('^\d{4}', product_author.text):
                                    print product_author.text
                    else:
                        print 'author not found'


                    print '--------------------------'
            except:
                print "some contents not found. Let's pass it."
                pass

        # 次のページヘのリンクを組み立てる
        base_url = 'http://www.amazon.co.jp/'
        next_path = next_page['href']
        next_url = '{base_url}{next_path}'.format(base_url=base_url, next_path=next_path)
        print next_url

        # scrapy.Request を返すと次にクロールするページの指定になる
        next_crawl_page = scrapy.Request(next_url)
        yield next_crawl_page
