import sqlite3


def create():
    c.execute("""CREATE TABLE subscriber
                 (id, chat_id PRIMARY KEY, subscribed_on)""")


db_path = r'subscriptions.sqlite3'
conn = sqlite3.connect(db_path)
c = conn.cursor()
create()
conn.commit()
c.close()
