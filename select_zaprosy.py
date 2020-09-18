# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 12:01:00 2020

@author: utrobinmv
"""

import os
import json

from database import db_connect, db_init, db_disconnect

connect = db_connect()

cursor = connect.cursor()

# Данный запрос получает выборку последних обновлений карты
command = (f"SELECT attrs_cn FROM map_update ORDER BY date_check DESC LIMIT 50")
cursor.execute(command)
for row in cursor:
    print("Select: ", row)

# Данный по владельцу объекта
attrs_cn = "59:10:0201006:3"
command = (f"SELECT attrs_cn, vid_kultur, sobstv_name, sobstv_inn, sobstv_addr, sobstv_phone FROM map_sobstv WHERE attrs_cn = '{attrs_cn}'")
cursor.execute(command)
for row in cursor:
    print("Select: ", row)

# Данный карты объекта
attrs_cn = "59:10:0201006:3"
command = (f"SELECT attrs_cn, date_foto, class_num, last_user_otvet, res_razmetka, url FROM map_objects WHERE attrs_cn = '{attrs_cn}'")
cursor.execute(command)
for row in cursor:
    print("Select: ", row)

# Данные росреестра
attrs_cn = "59:10:0201006:3"
command = (f"SELECT attrs_cn, date_check, class_num, last_user_otvet, res_razmetka, url FROM map_update WHERE attrs_cn = '{attrs_cn}'")
cursor.execute(command)
for row in cursor:
    print("Select: ", row)

# Изменение ответа пользователя по объекту
attrs_cn = "59:10:0201006:3"
last_user_otvet = 1
command = (f"UPDATE map_objects SET last_user_otvet = {last_user_otvet} WHERE attrs_cn = '{attrs_cn}'")
cursor.execute(command)


cursor.close()


db_disconnect(connect)