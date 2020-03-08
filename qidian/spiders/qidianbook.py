# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from qidian.items import QidianItem

#爬取起点小说网 作品信息并存入MySql
class QidianbookSpider(CrawlSpider):
    name = 'qidianbook'
    allowed_domains = ['book.qidian.com']
    start_urls = ['http://book.qidian.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/info/[0-9]{10}'), callback='parse_book', follow=True),#爬取url规则
    )

    def parse_book(self, response):
        #分析页面网站
        head = response.xpath("//div[@class='book-info ']")#总入口

        title = head.xpath(".//h1/em/text()").get()#文章标题
        author = head.xpath(".//h1/span/a/text()").get()#作者
        statu = head.xpath(".//p/span/text()").getall()#文章状态
        status=''
        for status1 in statu:
            status = status + status1 + ' '
        type1 = head.xpath(".//p[@class='tag']/a/text()").getall()#文章类别
        type=''
        for ty in type1:
            type = type + ty + ' '
        brief = head.xpath(".//p[@class='intro']/text()").get()#文章简介
        image = response.xpath(".//div[@class='book-img']//img/@src").get()#文章封面
        image = response.urljoin(image)
        contents = response.xpath(".//div[@class='book-intro']/p/text()").getall()#文章内容
        contents = list(map(lambda content:content.strip(),contents))
        content=''
        for content1 in contents:
            content = content+content1+'\n'
        url = response.url
        item = QidianItem(
            title = title,
            author = author,
            status = status,
            type = type,
            brief = brief,
            contents = content,
            image = image,
            url = url
        )
        yield item
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

