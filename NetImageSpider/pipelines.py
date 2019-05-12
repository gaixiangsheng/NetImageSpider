# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class NetimagespiderPipeline(ImagesPipeline):
    referer = ''
    headers = {
        'host': 'img.hi0590.com',
        'connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'referer': referer,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    }

    def process_item(self, item, spider):
        return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            self.referer = item['referer']
            print("image_url:", image_url)
            print("headers:", self.headers)
            yield scrapy.Request(image_url, headers=self.headers, meta={'item': item})

    def file_path(self, request, response=None, info=None):

        item = request.meta['item']
        dir_name = item['dir_name']
        dir_name = re.sub(r'[？\\*|“<>:/]', '', dir_name)

        img_name = item['name'].index(request.url)
        img_name = re.sub(r'[？\\*|“<>:/]', '', img_name)

        filename = u'/{0}/{1}'.format(dir_name, img_name)
        print("filename = ", filename)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        # item['image_paths'] = image_path
        return item
