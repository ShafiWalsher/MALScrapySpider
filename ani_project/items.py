# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeItem(scrapy.Item):
    uid     = scrapy.Field()
    title   = scrapy.Field()
    synopsis = scrapy.Field()
    img_url = scrapy.Field()
    link    = scrapy.Field()
    score   = scrapy.Field()
    ranked  = scrapy.Field()
    popularity  = scrapy.Field()
    members = scrapy.Field()
    aired   = scrapy.Field()
    genre   = scrapy.Field()
    episodes = scrapy.Field()

class ReviewItem(scrapy.Item):
    username    = scrapy.Field() 
    # profile     = scrapy.Field()
    anime_uid   = scrapy.Field()
    # text        = scrapy.Field()
    rating      = scrapy.Field()
    timestamp   = scrapy.Field()
    # scores      = scrapy.Field()

# class ProfileItem(scrapy.Item):
#     profile     = scrapy.Field()
#     gender      = scrapy.Field()
#     birthday    = scrapy.Field()
#     favorites   = scrapy.Field()
#     link        = scrapy.Field()    
