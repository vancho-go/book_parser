import scrapy
import os
from Bukvoed.items import BukvoedItem
from scrapy.loader import ItemLoader
import requests
from math import ceil
import re

images_dir = os.path.join(os.getcwd() + '/results/images/')

def download_image(url, SKU):
    filename = os.path.join(images_dir, SKU + '.' + url.split('.')[-1])
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)

class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = [f'https://www.bookvoed.ru/book?id={id}' for id in range(330516, 331620)]

    def parse(self, response):
        title = response.xpath('//h1/span/text()').extract()[0]
        image_link = 'https://www.bookvoed.ru' + response.xpath('//div/img/@src').extract_first()
        SKU = response.request.url[response.request.url.find('=')+1:]
        image_path = os.path.join(images_dir, SKU + '.' + image_link.split('.')[-1])
        tags = response.xpath('//div[@id="path"]/div/span/a/span/text()').extract()[3:]

        description_start_index = response.text.find('АННОТАЦИЯ')+40
        description_stop_index = description_start_index+response.text[description_start_index:description_start_index+4000].find('<div')-8
        description = response.text[description_start_index:description_stop_index]

        vendor_stop_index = response.text.rfind('выделите её мышкой') - 2
        vendor_start_index = response.text[:vendor_stop_index].rfind(title)

        vendor = response.text[vendor_start_index + len(title)+2:vendor_stop_index]

        if response.xpath('//div[@id="left_menu_buttons"]/div/div/div/text()').extract_first():
            price = response.xpath('//div[@id="left_menu_buttons"]/div/div/div/text()').extract_first()
            price = ceil(int(re.sub(r'[^0-9]', '', price)) * 1.5)
            download_image(image_link, SKU)
        else:
            price = 'out of stock'
        print(image_link)
        

        book = {
            'Title':title,
            'Body (HTML)':description,
            'Vendor':vendor,
            'Tags':tags,
            'Variant SKU':SKU,
            'Variant Price':price,
            'Image Src':image_path
        }
        yield book