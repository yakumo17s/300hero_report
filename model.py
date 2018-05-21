from peewee import (MySQLDatabase, Model, CharField)

db = MySQLDatabase(
    host='localhost',
    user='root',
    passwd='',
    charset='utf8',
    database='heroes'
)


class BaseModel(Model):
    class Meta:
        database = db


class Player(BaseModel):
    name = CharField()
    win = CharField()
    match_count = CharField()
    elo = CharField()
    level = CharField()
    update_time = CharField()
    rank = CharField()

    class Meta:
        table_name = 'player'


class PlayerData(BaseModel):
    name = CharField()
    match_id = CharField()
    hero = CharField()
    result = CharField()
    date = CharField()

    class Meta:
        table_name = 'player_data'


class GameData(BaseModel):
    match_id = CharField()
    head = CharField()
    kill_count = CharField()
    death = CharField()
    support = CharField()
    score = CharField()
    date = CharField()
    time = CharField()

    class Meta:
        table_name = 'game_data'


if __name__ == '__main__':
    tables = [
        Player,
        PlayerData,
        GameData
    ]
    db.connect()
    db.drop_tables(tables)
    db.create_tables(tables)
