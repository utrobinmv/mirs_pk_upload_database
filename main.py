# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:05:59 2020

Файл заполняет базу данных

@author: utrobinmv
"""

import os
import json
import zipfile
import base64

from database import db_connect, db_init, db_disconnect, db_insert_selhoz, db_insert_rosreestr, db_insert_img, db_insert_ndvi

connect = db_connect()

db_init(connect)

#Загрузка данных сельхоз земель (закомментировано так как загружаем разные таблицы в разное время)
# with open("data/result.json", "r") as read_file:
#     data = json.load(read_file)
#     for id_object in data:
#         el_obj = data[id_object]
#         db_insert_selhoz(connect, id_object, el_obj)

#Загрузка данных Росреестра (закомментировано так как загружаем разные таблицы в разное время)
# zipFile = zipfile.ZipFile('data/objects.zip', 'r')
# list_files = zipFile.namelist()
# for i, file_name in enumerate(list_files):
#     zipInfo = zipFile.getinfo(file_name)
#     if zipInfo.file_size > 0:
#         # zipFile.extract(file_name, "tmp", )
#         f = zipFile.read(file_name)
#         try:
#             f2 = json.loads(f)
#         except Exception as e:
#             print("File: " +  file_name + " error:" + str(e)) 
#         else:    
#             db_insert_rosreestr(connect, f2)
# zipFile.close()

#Загрузка данных Изображений (закомментировано так как загружаем разные таблицы в разное время)
# attrs_cn = ""
# zip = zipfile.ZipFile('data/images.zip', 'r')
# list_files = zip.namelist()
# for i, file_name in enumerate(list_files):
#     zipInfo = zip.getinfo(file_name)
#     if zipInfo.file_size > 0:
#         zip.extract(file_name, "tmp")
#         # f = zip.read(file_name)
#         file_name = "tmp/" + file_name
#         with open(file_name, 'rb') as f:
#             image = f.read()
#             tile = base64.b64encode(image).decode('ascii')    
#             # tile = image
#             if file_name.find("B08_cut") > 0:
#                 db_insert_img(connect, attrs_cn, "img_b08_cut", tile)
#             elif file_name.find("B04_cut") > 0:
#                 db_insert_img(connect, attrs_cn, "img_b04_cut", tile)
#             elif file_name.find("B04") > 0:
#                 db_insert_img(connect, attrs_cn, "img_b04", tile)
#             elif file_name.find("B08") > 0:
#                 db_insert_img(connect, attrs_cn, "img_b08", tile)
#             elif file_name.find("mask") > 0:
#                 db_insert_img(connect, attrs_cn, "img_mask", tile)
#             elif file_name.find("ndvi_cut") > 0:
#                 db_insert_img(connect, attrs_cn, "img_ndvi_cut", tile)
#             elif file_name.find("NDVI.txt") > 0:
#                 file_data = image.decode('ascii')
#                 ndvi = file_data.replace("{'data_field[0]': ", "").replace("}","")
#                 ndvi_float = float(ndvi)
#                 db_insert_ndvi(connect, attrs_cn, ndvi_float)
#             elif file_name.find("ndvi") > 0:
#                 db_insert_img(connect, attrs_cn, "img_ndvi", tile)
#             elif file_name.find("rr_cut") > 0:
#                 db_insert_img(connect, attrs_cn, "img_rr_cut", tile)
#             elif file_name.find("sat") > 0:
#                 db_insert_img(connect, attrs_cn, "img_sat", tile)
#     else:
#         folder = zipInfo
#         name_file = folder.filename
#         name_object = name_file.replace("images/", "").replace("/", "").replace("_", ":")
#         if name_object != "":
#             attrs_cn = name_object
# zip.close()

db_disconnect(connect)