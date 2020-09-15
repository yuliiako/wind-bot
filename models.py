import datetime

import peewee

import config

db = peewee.SqliteDatabase(config.DB_PATH)


class Subscriber(peewee.Model):
    class Meta:
        database = db

    chat_id = peewee.CharField()
    subscribed_on = peewee.DateTimeField(default=datetime.datetime.now)
