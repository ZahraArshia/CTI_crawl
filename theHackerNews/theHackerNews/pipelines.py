# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ThehackernewsPipeline:
    def open_spider(self, spider):
        # called when the spider is opened
        self.con = sqlite3.connect('hackerNews.db') # create a DB
        self.cur = self.con.cursor() 
        self.cur.execute('''DROP TABLE IF EXISTS hackerNews''') # drop table if already exists
        self.cur.execute('''CREATE TABLE hackerNews
                       (article text, link URL)''') # create a table
        self.con.commit()

    def close_spider(self, spider):
        # called when the spider is closed
        self.con.close()

    def process_item(self, item, spider):
        # called for each item crawled from spiders/quotes-spiders.py
        # insert the each item crawled into DB
        self.cur.execute("insert into hackerNews values (?, ?)", (item['article'], item['link']))
        self.con.commit()
        return item
