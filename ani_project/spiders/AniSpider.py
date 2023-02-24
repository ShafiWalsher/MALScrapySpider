# -*- coding: utf-8 -*-
import scrapy
import numpy as np
from ani_project.items import AnimeItem, ReviewItem
# https://myanimelist.net/topanime.php?limit=<limit>
# 
# scrapy runspider myanimelist/spiders/MyAnimeList.py 
# -a start_limit=<start_limit> 
# -a end_limit=<end_limit> 
# -s MONGODB_URL=<mongo_uri>
#
class MyAnimeListSpider(scrapy.Spider):
    name = 'aniSpider'
    allowed_domains = ['myanimelist.net']

    def start_requests(self):
        yield scrapy.Request('https://myanimelist.net/topanime.php?limit=%s' % self.start_limit) #16300

    # https://myanimelist.net/topanime.php
    def parse(self, response):
      self.logger.info('Parse function called on %s', response.url)

      limit = response.url.split("limit=")[1]
      if int(limit) > int(self.end_limit):
        return

      for rank in response.css(".ranking-list"):
        link    = rank.css("td.title a::attr(href)").extract_first()

        yield response.follow(link, self.parse_anime)

      next_page = response.css("a.link-blue-box.next::attr(href)").extract_first()
      if next_page is not None:
          yield response.follow("{}{}".format(response.url.split("?")[0], next_page), self.parse)

    # https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood
    def parse_anime(self, response):
      attr   = {}
      attr['link']   = response.url
      attr['uid']    = self._extract_anime_uid(response.url)
      attr['title']  = response.css("h1.title-name ::text").extract_first()
      attr['synopsis'] = " ".join(response.css("p[itemprop='description'] ::text").extract())
      attr['score']  = response.css("div.score ::Text").extract_first()
      attr['ranked'] = response.css("span.ranked strong ::Text").extract_first()
      attr['popularity'] = response.css("span.popularity strong ::Text").extract_first()
      attr['members'] = response.css("span.members strong ::Text").extract_first()
      attr['genre']   = response.css("div span[itemprop='genre'] ::text").extract()
      attr['img_url'] = response.css("a[href*=pics]>img::attr(src)").extract_first()

      status = response.css("td.borderClass div.spaceit_pad::text").extract()
      status = [i.replace("\n", "").strip() for i in status]

      attr['episodes'] = status[11].replace("\n","").strip()
      attr['aired']   = status[15].replace("\n","").strip()

      # / Anime
      yield AnimeItem(**attr)

      # /reviews
      yield response.follow("{}/{}".format(response.url, "reviews?p=1"), self.parse_review)


    # https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood/reviews?p=1
    def parse_review(self, response):
      p = response.url.split("p=")[1]

      reviews = response.css("div.review-element.js-review-element")
      for review in reviews:
        # link = review.css("div.review-element a::attr(href)").extract_first()
        # link = link + "/reviews"
        attr   = {}
        attr['username']       = response.css('div.username a::text').extract_first()
        attr['anime_uid'] = self._extract_anime_uid(response.css("a.hoverinfo_trigger ::attr(href)").extract_first())
        attr['rating']  = response.css("div.rating  span ::text").extract_first()
        attr['timestamp']  = response.css('div.body div.update_at::text').get() + "-" + response.css('div.body div.update_at::attr(title)').extract_first()
        yield ReviewItem(**attr)

        # yield response.follow(link, self.parse_review)

      # None, First Page and not last page
      next_page = response.css("div.mt4 a::attr(href)").extract()
      if next_page is not None and len(reviews) > 0 and len(next_page) > 0 and (p == '1' or len(next_page) > 1):
        next_page = next_page[0] if p == '1' else next_page[1]
        yield response.follow(next_page, self.parse_list_review)


    def _extract_anime_uid(self, url):
      return url.split("/")[4]

    def _list2dict(self, attrs):
      attrs = np.array(attrs)
      attrs = dict(zip(attrs[[i for i in range(len(attrs)) if (i%2) == 0]], 
                          attrs[[i for i in range(len(attrs)) if (i%2) == 1]] ))
      return attrs