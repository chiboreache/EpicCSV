"""
# * stays only for fallback purpose
# * use Firebase instead
"""

import sqlite3


db_path = 'db/uploadsCounter.db'


def dbInit():
    with sqlite3.connect(db_path) as db:
        c = db.cursor()
        c.execute(
"""CREATE TABLE IF NOT EXISTS t_uploads(
    TimeStamp          TEXT                     ,
    UploadCounter      INTEGER       PRIMARY KEY
                                                 )""")
        dbInsert(c)


def dbInsert(c):
    c.execute(
"""INSERT INTO t_uploads (TimeStamp)
    VALUES(datetime('now', '3 hours'))""")


def dbSelect(c):
    c.execute(
"""SELECT *
    FROM t_uploads
    WHERE UploadCounter = (
    SELECT MAX(UploadCounter)
    FROM t_uploads
                            )""")


if __name__ == '__main__':
    dbInit()
    print('Database created!')
