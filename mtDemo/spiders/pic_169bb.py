# -*- coding: utf-8 -*-
from scrapy.http import Request
import scrapy


class Pic169bbSpider(scrapy.Spider):
    # 爬虫（pic_169bb.py文件）会自动的先爬首页（169bb.com），爬完首页之后，会自动的进入parse()回调函数。
    # 这个回调函数中，我们需要写些东西
    name = 'pic_169bb'
    allowed_domains = ['169ku.com']
    start_urls = ['http://169ku.com/']

    def parse(self, response):
        # 以下
        urldata = response.xpath("/html/body/div[@class='header']/div[@class='hd_nav']/div[@class='w1000']//a/@href").extract()
        print(urldata)
        # 以上
        xiyangurldata = urldata[4]  # 获取西洋美女首页网址
        print(xiyangurldata)
        yield Request(url=xiyangurldata, callback=self.next)

    def next(self, response):
        page_title_list = response.xpath("/html/body//div[@class='w1000 box03']/ul[@class='product01']//li/a/@alt").extract()
        print(page_title_list)
        page_url_list = response.xpath("/html/body//div[@class='w1000 box03']/ul[@class='product01']//li/a/@href").extract()
        print(page_url_list)
        page_num = response.xpath("/html/body//div[@class='w1000 box03']//div[@class='page']/ul/li/a/@href").extract()[-1]
        # response.xpath("//span[@class='pageinfo']//strong/text()").extract()[0]  # 得到西洋美女总页数
        print(page_num)
        page_num = int(page_num[7-len(page_num):-5])  # 简单提取页码
        print(page_num)
        print(response.url)
        for i in range(1, int(page_num) + 1):
            page_url = response.url + 'list_4_' + str(i) + '.html'  # 得到西洋美女每一个页面的网址
            print(page_url)
            yield Request(url=page_url, callback=self.next2)
        pass

    def next2(self, response):  # 现在获取每一个美女的网页网址：
        page_title_list = response.xpath(
            "/html/body//div[@class='w1000 box03']/ul[@class='product01']//li/a/@alt").extract()
        # print(page_title_list)
        page_url_list = response.xpath(
            "/html/body//div[@class='w1000 box03']/ul[@class='product01']//li/a/@href").extract()
        # print(page_url_list)
        for i in range(0, len(page_url_list)):
            gril_page_url = page_url_list[i]
            print(gril_page_url)
            yield Request(url=gril_page_url, callback=self.next3)
        pass

    def next3(self, response):  # 得到一个美女网页里面的所有的页面的网址
        rela_pages_list = response.xpath("//div[@class='dede_pages']/ul//li/a/text()").extract()
        pages_num = len(rela_pages_list) - 3  # 借着翻页按键的个数来看有多少页
        # print(pages_num)
        self.getpic(response)
        if pages_num == -3:
            # pages_num = 1
            return
        for i in range(2, pages_num + 1):
            girl_page_url = response.url.replace('.html', '_') + str(i) + '.html'
            # print(girl_page_url)
            yield Request(url=girl_page_url, callback=self.getpic)
        pass

    def getpic(self, response):  # 获取每一个美女网页的每一个页面里面的所有高清图片
        # print(response.url)
        from mtDemo.items import MtdemoItem
        item = MtdemoItem()
        item['url'] = response.xpath("//div[@class='big-pic']/div[@class='big_img']//p/img/@src").extract()
        # print(item['url'])
        yield item
        pass
