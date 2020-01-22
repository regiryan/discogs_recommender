# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from ..items import DiscogsScrapeItem
from ..items import UserItem


class DiscogSpider(scrapy.Spider):
    name = 'user_lists'


    def start_requests(self):
        df = pd.read_csv('/Users/regi/Flatiron/final_project/discogs_scrape/test.csv')
        list_of_names = list(df.usernames)

        for name in list_of_names:
            collection_link = 'https://www.discogs.com/user/' + name + '/collection?page=1&limit=250'
            yield scrapy.Request(collection_link, callback=self.parse_collection)

    def parse_collection(self, response):

        items = CollectionsItem()

        all_titles = response.css('span.release_title')

        # page_releases = all_titles.xpath('.//a[contains(@href, "release")]/text()').getall()
        # page_artists = all_titles.xpath('.//a[contains(@href, "artist")]/text()').getall()
        # page_labels = all_titles.xpath('.//a[contains(@href, "label")]/text()').getall()
        # page_releases_links = all_titles.xpath('.//a[contains(@href, "release")]/@href').getall()
        page_ids = all_titles.xpath('.//a[contains(@href, "release")]/@href').re(r'release/(\d*)')
        page_ids = list(set(page_ids))

        user_name = response.css('.profile_username a::text').get()
        page_num = response.css('.hide_mobile strong::text').get()

        user_name_page = user_name + '-' + page_num
        items['coll_release_ids'] = page_ids
        items['username'] = user_name_page
        yield items

        next_page = response.css('.pagination_next::attr(href)').get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(next_page_link, callback=self.parse_collection)
        else:
            print(f'all_pages for user {user_name}')


def parse_wantlist(self, response):

    items = WantlistItem()

    all_titles = response.css('span.release_title')

    # page_releases = all_titles.xpath('.//a[contains(@href, "release")]/text()').getall()
    # page_artists = all_titles.xpath('.//a[contains(@href, "artist")]/text()').getall()
    # page_labels = all_titles.xpath('.//a[contains(@href, "label")]/text()').getall()
    # page_releases_links = all_titles.xpath('.//a[contains(@href, "release")]/@href').getall()
    page_ids = all_titles.xpath('.//a[contains(@href, "release")]/@href').re(r'release/(\d*)')
    page_ids = list(set(page_ids))

    user_name = response.css('.profile_username a::text').get()
    page_num = response.css('.hide_mobile strong::text').get()

    user_name_page = user_name + '-' + page_num
    items['coll_release_ids'] = page_ids
    items['username'] = user_name_page
    yield items

    next_page = response.css('.pagination_next::attr(href)').get()
    if next_page is not None:
        next_page_link = response.urljoin(next_page)
        yield scrapy.Request(next_page_link, callback=self.parse_collection)
    else:
        print(f'all_pages for user {user_name}')
