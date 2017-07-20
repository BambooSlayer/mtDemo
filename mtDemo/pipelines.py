# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import urllib.request


class MtdemoPipeline(object):
    def process_item(self, item, spider):  # 使用正则表达式得到图片下载网址的数字
        # print(len(item['url']))
        for i in range(0, len(item['url'])):
            this_url = item['url'][i]
            id = re.findall('http://724.169pp.net/169mm/(.*?).jpg', this_url)[0]  # 使用正则表达式得到图片下载网址的数字
            id = id.replace('/', '_')
            print(id)
            file = 'D:/FNNDP/xiyangmeinv/' + str(id) + '.jpg'
            print('Downloading :' , file)
            urllib.request.urlretrieve(this_url, filename=file)
            print('Final Download :' , file)
        return item
