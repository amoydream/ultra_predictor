# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from .items import Event, RaceResult, Race
import logging

HEADERS = {
    "Authorization": "Token f95a3f0be021fd2560ceef330adea7b5e6e4cf169551b625ca9302fd45cad8c6"
}
logger = logging.getLogger()


class ItraPipeline(object):
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, Race):
            for key in item.keys():
                if item[key] == "N/A":
                    item[key] = None

        if isinstance(item, Event):
            req = requests.post(
                "http://django:8000/api/events", headers=HEADERS, data=item
            )
            try:
                req.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error(f"Error EVENT: , req{req.content}, item: {item}")

        if isinstance(item, Race):
            logger.info(f"------SAVING RACE------\n{item}")
            req = requests.post(
                "http://django:8000/api/races", headers=HEADERS, data=item
            )
            try:
                req.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error(f"Error RACE:, req{req.content}, item: {item}")
        if isinstance(item, RaceResult):
            logger.info(f"------SAVING RACE RESULT------\n{item}")
            req = requests.post(
                 "http://django:8000/api/race_results", headers=HEADERS, data=item
            )
            try:
                req.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error(f"Error RACE RESULT:, req{req.content}, item: {item}")
        return item
