# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Event(scrapy.Item):
    name = scrapy.Field()
    itra_id = scrapy.Field()
    year = scrapy.Field()


class Race(scrapy.Item):
    name = scrapy.Field()
    itra_event_id = scrapy.Field()
    itra_race_id = scrapy.Field()
    itra_race_event_id  = scrapy.Field()
    itra_point = scrapy.Field()
    mount_point = scrapy.Field()
    finish_point = scrapy.Field()
    map_link = scrapy.Field()
    participation = scrapy.Field()
    sentiers = scrapy.Field()
    pistes = scrapy.Field()
    routes = scrapy.Field()
    challenge = scrapy.Field()
    championship = scrapy.Field()
    country_start = scrapy.Field()
    city_start = scrapy.Field()
    country_finish = scrapy.Field()
    city_finish = scrapy.Field()
    distance = scrapy.Field()
    race_date = scrapy.Field(serializer=str)   
    race_time = scrapy.Field()    
    ascent = scrapy.Field()
    descent = scrapy.Field()
    refreshment_points = scrapy.Field()
    max_time = scrapy.Field(serializer=str)


class RaceResult(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    time_result = scrapy.Field(serializer=str)
    position = scrapy.Field()
    sex = scrapy.Field()
    nationality = scrapy.Field()
    birth_year =  scrapy.Field()
    itra_race_id = scrapy.Field()
    itra_runner_id = scrapy.Field()
