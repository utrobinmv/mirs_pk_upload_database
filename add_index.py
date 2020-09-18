# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 10:05:59 2020

Добавление индексов в субд для ускорения

@author: utrobinmv
"""

import psycopg2

def db_connect():
    con = psycopg2.connect(dbname = "reestr", user='postgres', password='rossgress', port=5432, host='localhost')

    return con

def db_disconnect(con):
    con.commit()
    con.close()



connect = db_connect()

cursor = connect.cursor()

command = (f"CREATE INDEX attrs_cn_rosreestr_idx ON objects_rosreestr (attrs_cn);")
cursor.execute(command)

command = (f"CREATE INDEX attrs_cn_selhoz_idx ON objects_selhoz (attrs_cn);")
cursor.execute(command)

command = (f"CREATE INDEX attrs_cn_map_images_idx ON map_images (attrs_cn);")
cursor.execute(command)

command = (f"CREATE INDEX attrs_cn_map_update_idx ON map_update (attrs_cn);")
cursor.execute(command)

cursor.close()

db_disconnect(connect)

