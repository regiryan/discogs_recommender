# -*- coding: utf-8 -*-
import scrapy
from ..items import DiscogsScrapeItem

class DiscogSpider(scrapy.Spider):
    name = 'discog'
    # allowed_domains = ['discogs.com']
    start_urls = ['https://www.discogs.com/group/114/members',
                    'https://www.discogs.com/group/451', 'https://www.discogs.com/group/1165', 'https://www.discogs.com/group/7373/members',
                  'https://www.discogs.com/group/575']
    # page_number = 2

    # def parse(self, response):
    #
    #     # items = DiscogsScrapeItem()
    #     for url in start_urls:
    #         yield scrapy.Request(url, callback=self.parse_group())
        # all_groups = response.css('div.group-list-group-content')
        #
        # for group in all_groups:
        #     group_link = group.css('a.section_link::attr(href)').extract_first()
        #     group_members_link = 'https://www.discogs.com' + group_link + '/members?page=1&limit=50'
        #     # items['link'] = group_link
        #     # print(items['link'])
        #     #[{'name': 'Emre', 'link': 'www.link.com/link/1'}, {'name': 'Emre', 'link': 'www.link.com/link/1'}]
        #     yield scrapy.Request(group_members_link, callback=self.parse_group)

        # next_page = response.css('.pagination_next::attr(href)').get()

        # if DiscogSpider.page_number <= 74:
        #     next_page = f'https://www.discogs.com/group/browse/all?limit=54&page={DiscogSpider.page_number}'
        #     DiscogSpider.page_number += 1
        #     # next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback = self.parse)
# https://www.discogs.com/group/9/members
    def parse(self, response):

        # group_items = DiscogsScrapeItem()

        # user_links = response.css('.users-list a::attr(href)').extract()
        user_links = response.css('.users-list li')

        next_page = response.css('.pagination_next::attr(href)').get()

        for link in user_links:
            href_link = link.css('a.thumbnail_link').attrib['href']
            user_page_link = 'https://www.discogs.com' + href_link
            yield scrapy.Request(user_page_link, callback = self.parse_user)

        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback = self.parse)


    def parse_user(self, response):
        keys = ['For Sale', 'Contributed', 'In Collection', 'In Wantlist', 'Images', 'Reviews', 'Lists']
        items = DiscogsScrapeItem()

        user_elements = response.css('.profile_sections li')
        section_links = user_elements.css('a::attr(href)').extract()
        sections_list = user_elements.css('a::text').extract()
        sections_list = [section.strip() for section in sections_list]
        sections_list = [section for section in sections_list if section != '']
        # print(f'sections list is : {sections_list}')
        user_dict = dict(zip(sections_list, section_links))
        # print(user_dict)
        if 'For Sale' in sections_list:
            items['for_sale'] = user_dict['For Sale']
        else:
            items['for_sale'] = 'none'
        if 'Contributed' in sections_list:
            items['contributed'] = user_dict['Contributed']
        else:
            items['contributed'] = 'none'
        if 'In Collection' in sections_list:
            items['in_collection'] = user_dict['In Collection']
        else:
            items['in_collection'] = 'none'
        if 'In Wantlist' in sections_list:
            items['in_wantlist'] = user_dict['In Wantlist']
        else:
            items['in_wantlist'] = 'none'
        if 'Reviews' in sections_list:
            items['reviews'] = user_dict['Reviews']
        else:
            items['reviews'] = 'none'
        if 'Images' in sections_list:
            items['images'] = user_dict['Images']
        else:
            items['images'] = 'none'
        if 'Lists' in sections_list:
            items['lists'] = user_dict['Lists']
        else:
            items['lists'] = 'none'

        username = response.css('.profile_username a::text').extract_first()
        items['username'] = username
        # print(items)
        yield items
