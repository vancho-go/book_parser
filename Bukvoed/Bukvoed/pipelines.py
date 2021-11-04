# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os 


template_dir = os.path.join(os.getcwd() + '/results/templates/')
result_dir = os.path.join(os.getcwd() + '/results/')
images_dir = os.path.join(os.getcwd() + '/results/images/')
previous_db = os.path.join(os.getcwd() + '/results/prev_db.csv')

reader_prev = [book['Title'] for book in csv.DictReader(open(previous_db, 'r', encoding='UTF-8'))]

if not os.path.exists(result_dir):os.mkdir(result_dir)
if not os.path.exists(images_dir):os.mkdir(images_dir)

class BukvoedPipeline:
    def process_item(self, item, spider):
        if not item['Title'] in reader_prev and not item['Variant Price'] =='out of stock':
            with open(os.path.join(result_dir + 'bookscsv.csv'), 'a', encoding='UTF-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=item)
                writer.writerow(item)

        elif item['Title'] in reader_prev and item['Variant Price'] =='out of stock':
            with open(os.path.join(result_dir + 'bookscsv_delete.csv'), 'a', encoding='UTF-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=item.keys())
                writer.writerow(item)
        return item
