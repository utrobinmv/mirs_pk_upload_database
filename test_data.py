# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:05:59 2020

Файл заполняет тестовую выборку объектов для обновления

@author: utrobinmv
"""

from database import db_connect, db_init, db_disconnect
import datetime



connect = db_connect()

cursor = connect.cursor()

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d")

# command = (f"TRUNCATE TABLE map_update")
# cursor.execute(command)

attrs_cn = "59:10:0201006:3"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.7, 1, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0501003:98"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.5, 2, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0601002:2"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.2, 1, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0601002:3"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.6, 2, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0601047:17"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.2, 1, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0601047:20"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.2, 1, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0602012:12"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.2, 1, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0602012:4"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.2, 1, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

attrs_cn = "59:10:0602037:7"
command = (f"INSERT INTO map_update (attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url, attrs_id) VALUES ('{attrs_cn}', '{now_str}', 0.2, 1, 0, '', '', '{attrs_cn}')")
cursor.execute(command)

cursor.close()

db_disconnect(connect)