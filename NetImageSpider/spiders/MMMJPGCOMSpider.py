# -*- coding: utf-8 -*-

import scrapy
import re
import time

from NetImageSpider.items import NetimagespiderItem
from NetImageSpider.settings import USER_AGENT


class MMMJPGCOMSpider(scrapy.Spider):
    name = "mmmjpgcom"
    allowed_domains = ["www.mmmjpg.com"]
    start_urls = ['http://www.mmmjpg.com/more/']
    referer = 'http://www.mmmjpg.com/more/'

    headers = {
        'host': 'www.mmmjpg.com',
        'connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'referer': referer,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cookie': 'Hm_lvt_d328bd83aff58d726c1a6fb64991331b=1557559863,1557581053; Hm_lpvt_d328bd83aff58d726c1a6fb64991331b=' + str(
            int(time.time())),
    }

    cookie = {}

    ## 解析更多美女标签
    def parse(self, response):
        list = response.xpath("//div/div[@class='tag']/ul/li")
        hrefLists = []
        for item in list:
            href = item.xpath("./a/@href").extract_first()
            dir_count = item.xpath('./i/text()').extract_first()
            pattern = re.compile(r'\d+')
            count = pattern.findall(dir_count)

            pageNo = int(int(count[0]) / 21)
            if pageNo <= 0:
                hrefs = "http://www.mmmjpg.com" + href
                hrefLists.append(hrefs)
                yield scrapy.Request(hrefs, headers=self.headers, callback=self.parsePage)
            else:
                for page in range(1, pageNo + 1):
                    hrefs = "http://www.mmmjpg.com" + href + "/" + str(page)
                    hrefLists.append(hrefs)
                    yield scrapy.Request(hrefs, callback=self.parsePage)


    ## 解析单个页面
    def parsePage(self, response):
        list = response.xpath("//div/ul/li")

        for item in list:
            href = item.xpath("./a/@href").extract_first()
            yield scrapy.Request("http://www.mmmjpg.com" + href, callback=self.parseImage)

    def parseImage(self, response):
        name = response.xpath("//div/div/h1/text()").extract_first()
        javascript = response.xpath("//div[@class='clearfloat']/script[@type='text/javascript']/text()").extract_first()
        pattern = re.compile(r'http://img.hi0590.com/\d+/\d+.jpg')
        imageHrefs = pattern.findall(javascript)

        index = 0
        item = NetimagespiderItem()
        item['referer'] = response.url
        item['dir_name'] = name
        item['name'] = []
        item['image_urls'] = []

        for imgHref in imageHrefs:
            item['name'].append(name + "(图" + str(index) + ")")
            item['image_urls'].append(imgHref)
            index += 1

        if len(item['image_urls']) > 0:
            yield item
