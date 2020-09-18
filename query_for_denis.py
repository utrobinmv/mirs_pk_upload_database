# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 10:05:59 2020

Запросы для различных выборок

@author: utrobinmv
"""

import psycopg2
import base64
import datetime

def db_connect():
    con = psycopg2.connect(dbname = "reestr", user='postgres', password='rossgress', port=5432, host='localhost')

    return con

def db_disconnect(con):
    # con.commit()
    con.close()

def select_image(con, map_col, cn):
    cursor = con.cursor()

    command = (f"SELECT {map_col} FROM map_images WHERE attrs_cn = '{cn}'")
    cursor.execute(command)
    for row in cursor:
        # print("Image: ", row[0])
        data64 = row[0]
        image = base64.b64decode(data64)
        return image

    cursor.close()


def add_update(con, attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url):

    cursor = con.cursor()

    command = (f"SELECT attrs_cn from map_update where attrs_cn = '{attrs_cn}'")
    cursor.execute(command)
    results = cursor.fetchall()
    if len(results) > 0:
        f = 1
    else:
        command = (f"INSERT INTO map_update (attrs_cn, attrs_id) VALUES ('{attrs_cn}', '{attrs_cn}');")
        cursor.execute(command)

    command = (f'''UPDATE map_update SET  
        date_check = '{date_check}',
        new_ndvi = {new_ndvi},
        class_num = {class_num},
        last_user_otvet = {last_user_otvet},
        res_razmetka = '{res_razmetka}',
        url = '{url}'
        where attrs_cn= '{attrs_cn}';''')
    cursor.execute(command)

    cursor.close()
    con.commit()

def update_button(con, attrs_cn, last_user_otvet): # last_user_otvet = 1 - ответ Подтвердить, 2 - Отклонить, 3 - Гипотеза ошибочна

    cursor = con.cursor()

    new_ndvi = 0

    command = (f"SELECT attrs_cn, new_ndvi from map_update where attrs_cn = '{attrs_cn}'")
    cursor.execute(command)
    results = cursor.fetchall()
    if len(results) > 0:
        new_ndvi = results[0][1]
    else:
        return    

    #записываем данные ответа в таблицу (не обзяательно, если запись потом будет удалена)
    command = (f'''UPDATE map_update SET  
        last_user_otvet = {last_user_otvet}
        where attrs_cn= '{attrs_cn}';''')
    cursor.execute(command)

    #Обновляем запись новый ndvi в таблицу земель
    if last_user_otvet == 1:
        command = (f'''UPDATE objects_selhoz SET  
            ndvi = {new_ndvi}
            where attrs_cn= '{attrs_cn}';''')
        cursor.execute(command)

    #Удаляем запись из таблицы, если нужно?
    if last_user_otvet == 1:
        command = (f'''DELETE FROM map_update where attrs_cn= '{attrs_cn}';''')
        cursor.execute(command)
        

    cursor.close()

    con.commit()


connect = db_connect()

attrs_cn = "59:10:0201006:3"
update_button(connect, attrs_cn, 1)

#Добавление объектв в апдейт
# attrs_cn = "59:10:0201006:3"
# date_check = datetime.datetime.now().strftime("%Y-%m-%d")
# new_ndvi = 0.2
# class_num = 1
# last_user_otvet = 1
# res_razmetka = ""
# url = ""
# add_update(connect, attrs_cn, date_check, new_ndvi, class_num, last_user_otvet, res_razmetka, url)

#Получение картинки из базы
# map_col = "img_B08_cut"
# map_col = "img_B04_cut"
# map_col = "img_B04"
# map_col = "img_B08"
# map_col = "img_mask"
# map_col = "img_ndvi_cut"
# map_col = "img_ndvi"
# map_col = "img_rr_cut"
# map_col = "img_sat"
# attrs_cn = "59:10:0602012:4"
# image = select_image(connect, map_col, attrs_cn)
# with open("img.png", "wb") as file:
#     file.write(image)



db_disconnect(connect)
