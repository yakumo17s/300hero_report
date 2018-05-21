# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jump_300heroes.items import Player, ResultList, GameResult
from db import db_handle
from model import PlayerData, Player as Player_model, GameData


class Jump300HeroesPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, Player):
            query = Player_model.select().where(
                Player_model.name == item['name'])

            if len(query):
                Player_model.update(
                    win=item['win'], match_count=item['match_count'],
                    elo=item['elo'], level=item['level'],
                    update_time=item['update_time']).where(
                    Player_model.name == item['name']).execute()
            else:
                Player_model.insert(
                    name=item['name'], level=item['level'], win=item['win'],
                    match_count=item['match_count'],
                    update_time=item['update_time'], elo=item['elo']
                ).execute()

        if isinstance(item, ResultList):
            PlayerData.insert(
                name=item['name'], match_id=item['match_id'],
                hero=item['hero'], result=item['result'], date=item['date']
            ).execute()

        if isinstance(item, GameResult):
            GameData.insert(
                name=item['name'], match_id=item['match_id'],
                head=item['head'], kill_count=item['kill'], death=item['death'],
                support=item['support'], score=item['score'],
                date=item['date'], time=item['time'], role=item['role'],
                level=item['level'], result=item['result']).execute()

        return item
