# -*- coding: utf-8 -*-
import scrapy
import hashlib
from bitco_in_forum.items import BitcoInForumItem


class BitcoInforumSpider(scrapy.Spider):
    name = 'Bitco_inForum'
    allowed_domains = ['bitco.in/forum/']
    start_urls = ['http://bitco.in/forum//']

    def parse(self, response):
        subforums = response.css("div.nodeText h3.nodeTitle a::attr(href)").extract()
        for board in subforums:
            yield scrapy.Request(url=board,
                                 callback=self.parse_topics)

    def parse_topics(self, response):
        topic_links = response.css("h3.title a::attr(href)").extract()

        try:
            page_list = response.css("div.PageNav a::text").extract()

            counter = 0

            # index finden
            for element in page_list:
                if page_list[counter] != "Next >":
                    counter = counter + 1
                    continue
                else:
                    break

            next_url = response.css("div.PageNav a::attr(href)").extract()[counter]

            if next_url is not None:
                yield scrapy.Request(url=next_url,
                                     callback=self.parse_topics)

            for topic_link in topic_links:
                yield scrapy.Request(url=topic_link,
                                     callback=self.parse_posts)
        except:
            # no text
            pass

    def parse_posts(self, response):
        post = BitcoInForumItem()

        author_list = response.css("div.uix_usernameWrapper a::text").extract()
        topic_list = response.css("div.titleBar h1::text").extract()
        dates_list = response.css("span.DateTime::text").extract()
        posttext_list = response.css("blockquote.messageText::text")

        for idx, item in enumerate(author_list):
            try:
                post['author'] = author_list[idx]
            except:
                post['author'] = "None"

            try:
                post['datetime'] = dates_list[idx]
            except:
                post['datetime'] = "None"

            try:
                post['posttext'] = posttext_list[idx]
            except:
                post['posttext'] = "None"

            try:
                post['topic'] = topic_list[idx]
            except:
                post['topic'] = "None"

            tohash = str(post['author']) + str(post['datetime']) + str(post['posttext']) + str(post['topic'])
            hobject = hashlib.sha256(tohash.encode())
            hash_string = str(hobject.hexdigest())
            post['identityhash'] = hash_string

            yield post

        # Pagination
        try:
            next_page_array = response.css("div.PageNav a::text").extract()

            counter = 0
            # index finden
            for element in next_page_array:
                if next_page_array[counter] != "Next >":
                    counter = counter + 1
                    continue
                else:
                    break

            next_url = response.css("div.PageNav a::attr(href)").extract()[counter]

        except:
            next_url = None

        if next_url is not None:
            yield scrapy.Request(url=next_url,
                                 callback=self.parse_posts)
