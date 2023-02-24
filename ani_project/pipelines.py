# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os
import numpy as np
from ani_project.items import AnimeItem, ReviewItem

class ProcessPipeline(object):

    def open_spider(self, spider):
      pass

    def close_spider(self, spider):
      pass

    def process_item(self, item, spider):
      item_class = item.__class__.__name__

      if item_class == "AnimeItem":
        item = self.process_anime(item)
      elif item_class == "ReviewItem":
        item = self.process_review(item)
      elif item_class == "ProfileItem":
        item = self.process_profile(item)

      return item

    def process_anime(self, item):
      if 'N/A' in item['score']:
        item['score'] = np.nan
      else:
        item['score'] = float(item['score'].replace("\n", "").strip())
      
      if item['ranked'] == 'N/A':
        item['ranked'] = np.nan
      else:
        item['ranked']     = int(item['ranked'].replace("#", "").strip())
      
      item['popularity'] = int(item['popularity'].replace("#", "").strip())
      item['members']    = int(item['members'].replace(",", "").strip())
      item['episodes']   = item['episodes'].replace(",", "").strip()

      return item

    def process_review(self, item):
      item['score']      = float(item['score'].replace("\n", "").strip())

      return item

    def process_profile(self, item):

      return item

class SaveLocalPipeline(object):

    def open_spider(self, spider):
      os.makedirs('data/', exist_ok=True)

      self.files = {}
      self.files['AnimeItem']   = open('data/animes.json', 'w+')
      self.files['ReviewItem']  = open('data/reviews.json', 'w+')
      self.files['ProfileItem'] = open('data/profiles.json', 'w+')

    def close_spider(self, spider):
      for k, v in self.files.items():
        v.close()

    def process_item(self, item, spider):
      item_class = item.__class__.__name__

      # Save
      self.save(item_class, item)

      return item

    def save(self, item_class, item):
      line =  json.dumps(dict(item)) + '\n'
      self.files[item_class].write(line)
