# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jump_300heroes.items import Player, ResultList, GameResult
from db import db_handle


class Jump300HeroesPipeline(object):

    def process_item(self, item, spider):
        db = db_handle()
        print('存储')
        print(item)
        with db as cur:

            if isinstance(item, Player):
                sql = 'insert into player(name, level, win, match_count, update_time, rank, elo)' \
                      ' values(%s, %s, %s, %s, %s, %s ,%s)'
                cur.execute(sql, (item['name'], item['level'], item['win'], item['match_count'],
                                  item['update_time'], item['rank'], item['strength']))

            if isinstance(item, ResultList):
                sql = 'insert into player_data(name, match_id, hero, result, date) values(%s, %s, %s, %s, %s)'
                cur.execute(sql, (item['name'], item['match_id'], item['hero'], item['result'], item['date']))

            if isinstance(item, GameResult):
                sql = 'insert into game_data(match_id, head, kill_count, death, support, score, date, time)' \
                      ' values(%s, %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(sql, (item['match_id'], item['head'], item['kill'], item['death'], item['support'],
                                  item['score'], item['date'], item['time']))

            return item
