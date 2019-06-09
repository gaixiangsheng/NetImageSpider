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
        'host': 'img.mmmjpg.com',
        'connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'referer': referer,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    }

    def get_media_requests(self, item, info):

        image_url_len = len(item['image_urls'])
        # print("本次下载：", image_url_len)
        for index in range(0, image_url_len):
            self.referer = item['referer']
            # print("目录：", item['dir_name'])
            # print("文件名：", item['name'][index])
            # print("下载地址：", item['image_urls'][index])
            yield scrapy.Request(item['image_urls'][index],
                                 headers=self.headers,
                                 meta={"image_name": item['name'][index], "dir_name": item['dir_name']})

    def file_path(self, request, response=None, info=None):
        dir_name = request.meta['dir_name']
        dir_name = re.sub(r'[？?\\*|“<>:/]', '', dir_name)

        img_name = request.meta['image_name']
        img_name = re.sub(r'[？?\\*|“<>:/]', '', img_name)

        filename = u'/{0}/{1}.jpg'.format(dir_name, img_name)
        print("filename = ", filename)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        # item['image_paths'] = image_path
        return item
