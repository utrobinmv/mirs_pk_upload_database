# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:05:59 2020

@author: utrobinmv
"""

import psycopg2
import json

def db_connect():
    con = psycopg2.connect(dbname = "reestr", user='postgres', password='rossgress', port=5432, host='localhost')

    return con

def create_table(con):
    commands = (
        # """ DROP TABLE IF EXISTS image_mask
        # """,
        # """ DROP TABLE IF EXISTS map_objects
        # """,
        # """ DROP TABLE IF EXISTS map_update
        # """,
        # """ DROP TABLE IF EXISTS image_mapsat
        # """,
        # """ DROP TABLE IF EXISTS objects_selhoz
        # """,
        # """ DROP TABLE IF EXISTS objects
        # """,
        # """ DROP TABLE IF EXISTS map_images
        # """,
        # """ DROP TABLE IF EXISTS objects_rosreestr
        # """,
        """
        CREATE TABLE IF NOT EXISTS objects_rosreestr (
            attrs_cn VARCHAR(40) NOT NULL PRIMARY KEY,
            type INTEGER,
            attrs_address VARCHAR(2000),
            extent_xmin NUMERIC(18, 10),
            extent_xmax NUMERIC(18, 10),
            extent_ymin NUMERIC(18, 10),
            extent_ymax NUMERIC(18, 10),
            center_x NUMERIC(18, 10),
            center_y NUMERIC(18, 10),
            attrs_category_type VARCHAR(40),
            attrs_statecd VARCHAR(10), 
            attrs_rifr_cnt VARCHAR(40),
            attrs_area_type VARCHAR(10),
            attrs_application_date VARCHAR(20), 
            attrs_rifr VARCHAR(40), 
            attrs_rifr_dep_info VARCHAR(40),
            attrs_is_big BOOLEAN, 
            attrs_kvartal_cn VARCHAR(40),
            attrs_fp VARCHAR(40),
            attrs_area_value VARCHAR(40),
            attrs_sale_cnt VARCHAR(40),
            attrs_util_code VARCHAR(40),
            attrs_date_cost VARCHAR(40),
            attrs_kvartal VARCHAR(40),
            attrs_cc_date_approval VARCHAR(40),
            attrs_sale_dep_uo VARCHAR(40),
            attrs_rifr_dep VARCHAR(40),
            attrs_area_unit VARCHAR(40),
            attrs_cc_date_entering VARCHAR(40),
            attrs_sale_date VARCHAR(40),
            attrs_sale_price VARCHAR(40),
            attrs_sale VARCHAR(40),
            attrs_sale_doc_date VARCHAR(40),
            attrs_cad_cost VARCHAR(40),
            attrs_cad_unit VARCHAR(40),
            attrs_sale_dep VARCHAR(40),
            attrs_children VARCHAR(40),
            attrs_parcel_type VARCHAR(40),
            attrs_sale_doc_num VARCHAR(40),
            attrs_sale_doc_type VARCHAR(40),
            attrs_util_by_doc VARCHAR(2800),
            attrs_id VARCHAR(40) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS objects_selhoz (
            attrs_cn VARCHAR(40) NOT NULL PRIMARY KEY,
            extent_xmin NUMERIC(18, 10),
            extent_xmax NUMERIC(18, 10),
            extent_ymin NUMERIC(18, 10),
            extent_ymax NUMERIC(18, 10),
            ndvi real,
            util_code VARCHAR(40),
            category_type VARCHAR(40),
            center_x NUMERIC(18, 10),
            center_y NUMERIC(18, 10),
            attrs_id VARCHAR(40) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS map_sobstv (
            attrs_cn VARCHAR(40) NOT NULL PRIMARY KEY,
            vid_kultur INTEGER,
            sobstv_name VARCHAR(100),
            sobstv_inn VARCHAR(20),
            sobstv_addr VARCHAR(100),
            sobstv_phone VARCHAR(100),
            attrs_id VARCHAR(40) NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS map_images (
                attrs_cn VARCHAR(40) NOT NULL PRIMARY KEY,
                ndvi real, 
                img_mask text, 
                img_ndvi text, 
                img_ndvi_cut text, 
                img_rr_cut text, 
                img_sat text, 
                img_b04 text, 
                img_b04_cut text, 
                img_b08 text, 
                img_b08_cut text 
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS map_update (
            attrs_cn VARCHAR(40) NOT NULL PRIMARY KEY,
            date_check date,
            new_ndvi real,
            class_num INTEGER,
            last_user_otvet INTEGER, 
            res_razmetka VARCHAR(200),
            url VARCHAR(400),
            attrs_id VARCHAR(40) NOT NULL
        )
        """
     )

    #ALTER TABLE `settings` ADD COLUMN IF NOT EXISTS `multi_user` TINYINT(1) NOT NULL DEFAULT 1

    cursor = con.cursor()

    for command in commands:
        cursor.execute(command)

    cursor.close()
    
def db_init(con):
    create_table(con)

def db_insert_selhoz(con, id_object, record):

    feature = record['util_code']
    if feature == None:
        return

    extent = record['category_type']
    if extent == None:
        return

    attrs_cn = id_object
    attrs_id = id_object
    
    extent_xmin = record['xmin']
    extent_xmax = record['xmax']
    extent_ymin = record['ymin']
    extent_ymax = record['ymax']
    center_x = record['x']
    center_y = record['y']
    util_code = record['util_code']
    category_type = record['category_type']

    cursor = con.cursor()

    command = (f"INSERT INTO objects_selhoz (attrs_cn, attrs_id) VALUES ('{attrs_cn}', '{attrs_id}');")
    cursor.execute(command)
    command = (f'''UPDATE objects_selhoz SET  
        extent_xmin ='{extent_xmin}',
        extent_xmax ='{extent_xmax}',
        extent_ymin ='{extent_ymin}',
        extent_ymax ='{extent_ymax}',
        center_x ='{center_x}',
        center_y ='{center_y}',
        category_type ='{category_type}',
        util_code ='{util_code}'
        where attrs_cn='{attrs_cn}';''')
    cursor.execute(command)

    cursor.close()

def db_insert_img(con, id_object, col_name, record):

    attrs_cn = id_object
    
    cursor = con.cursor()

    command = (f"SELECT attrs_cn from map_images where attrs_cn = '{attrs_cn}'")
    cursor.execute(command)
    results = cursor.fetchall()
    if len(results) > 0:
        f = 1
    else:
        command = (f"INSERT INTO map_images (attrs_cn) VALUES ('{attrs_cn}');")
        cursor.execute(command)

    # valClause = psycopg2.Binary(record)
    valClause = record
    command = f"UPDATE map_images SET {col_name} = '{valClause}' where attrs_cn='{attrs_cn}'"
    cursor.execute(command)

    cursor.close()

def db_insert_ndvi(con, id_object, ndvi):

    attrs_cn = id_object
    
    cursor = con.cursor()

    command = (f"SELECT attrs_cn from map_images where attrs_cn = '{attrs_cn}'")
    cursor.execute(command)
    results = cursor.fetchall()
    if len(results) > 0:
        f = 1
    else:
        command = (f"INSERT INTO map_images (attrs_cn) VALUES ('{attrs_cn}');")
        cursor.execute(command)

    command = f"UPDATE map_images SET ndvi = {ndvi} where attrs_cn='{attrs_cn}'"
    cursor.execute(command)

    cursor.close()




def db_insert_rosreestr(con, record):

    feature = record['feature']
    if feature == None:
        return

    extent = record['feature']['extent']
    if extent == None:
        return

    # s = 1
    attrs_cn = record['feature']['attrs']['cn']
    attrs_id = record['feature']['attrs']['id']
    
    type_num = record['feature']['type']

    attrs_address = record['feature']['attrs']['address']
    extent_xmin = record['feature']['extent']['xmin']
    extent_xmax = record['feature']['extent']['xmax']
    extent_ymin = record['feature']['extent']['ymin']
    extent_ymax = record['feature']['extent']['ymax']
    center_x = record['feature']['center']['x']
    center_y = record['feature']['center']['y']
    attrs_category_type = record['feature']['attrs']['category_type']
    attrs_statecd = record['feature']['attrs']['statecd'] 
    attrs_rifr_cnt = record['feature']['attrs']['rifr_cnt']
    attrs_area_type = record['feature']['attrs']['area_type']
    attrs_application_date = record['feature']['attrs']['application_date'] 
    attrs_rifr = record['feature']['attrs']['rifr'] 
    attrs_rifr_dep_info = record['feature']['attrs']['rifr_dep_info']
    attrs_is_big = record['feature']['attrs']['is_big']
    attrs_kvartal_cn = record['feature']['attrs']['kvartal_cn']
    attrs_fp = record['feature']['attrs']['fp']
    attrs_area_value = record['feature']['attrs']['area_value']
    attrs_sale_cnt = record['feature']['attrs']['sale_cnt']
    attrs_util_code = record['feature']['attrs']['util_code']
    attrs_date_cost = record['feature']['attrs']['date_cost']
    attrs_kvartal = record['feature']['attrs']['kvartal']
    attrs_cc_date_approval = record['feature']['attrs']['cc_date_approval']
    attrs_sale_dep_uo = record['feature']['attrs']['sale_dep_uo']
    attrs_rifr_dep = record['feature']['attrs']['rifr_dep']
    attrs_area_unit = record['feature']['attrs']['area_unit']
    attrs_cc_date_entering = record['feature']['attrs']['cc_date_entering']
    attrs_sale_date = record['feature']['attrs']['sale_date']
    attrs_sale_price = record['feature']['attrs']['sale_price']
    attrs_sale = record['feature']['attrs']['sale']
    attrs_sale_doc_date = record['feature']['attrs']['sale_doc_date']
    attrs_cad_cost = record['feature']['attrs']['cad_cost']
    attrs_cad_unit = record['feature']['attrs']['cad_unit']
    attrs_sale_dep = record['feature']['attrs']['sale_dep']
    attrs_children = record['feature']['attrs']['children']
    attrs_parcel_type = record['feature']['attrs']['parcel_type']
    attrs_sale_doc_num = record['feature']['attrs']['sale_doc_num']
    attrs_sale_doc_type = record['feature']['attrs']['sale_doc_type']
    attrs_util_by_doc = record['feature']['attrs']['util_by_doc']

    cursor = con.cursor()

    # command = (f"INSERT INTO objects SET attrs_cn='{attrs_cn}';")
    command = (f"INSERT INTO objects_rosreestr (attrs_cn, attrs_id) VALUES ('{attrs_cn}', '{attrs_id}');")
    cursor.execute(command)


    command = (f'''UPDATE objects_rosreestr SET type='{type_num}', 
        attrs_address='{attrs_address}',
        extent_xmin ='{extent_xmin}',
        extent_xmax ='{extent_xmax}',
        extent_ymin ='{extent_ymin}',
        extent_ymax ='{extent_ymax}',
        center_x ='{center_x}',
        center_y ='{center_y}',
        attrs_category_type ='{attrs_category_type}',
        attrs_statecd ='{attrs_statecd}' ,
        attrs_rifr_cnt ='{attrs_rifr_cnt}',
        attrs_area_type ='{attrs_area_type}',
        attrs_application_date ='{attrs_application_date}',
        attrs_rifr ='{attrs_rifr}',
        attrs_rifr_dep_info ='{attrs_rifr_dep_info}',
        attrs_is_big ='{attrs_is_big}',
        attrs_kvartal_cn ='{attrs_kvartal_cn}',
        attrs_fp ='{attrs_fp}',
        attrs_area_value ='{attrs_area_value}',
        attrs_sale_cnt ='{attrs_sale_cnt}',
        attrs_util_code ='{attrs_util_code}',
        attrs_date_cost ='{attrs_date_cost}',
        attrs_kvartal ='{attrs_kvartal}',
        attrs_cc_date_approval ='{attrs_cc_date_approval}',
        attrs_sale_dep_uo ='{attrs_sale_dep_uo}',
        attrs_rifr_dep ='{attrs_rifr_dep}',
        attrs_area_unit ='{attrs_area_unit}',
        attrs_cc_date_entering ='{attrs_cc_date_entering}',
        attrs_sale_date ='{attrs_sale_date}',
        attrs_sale_price ='{attrs_sale_price}',
        attrs_sale ='{attrs_sale}',
        attrs_sale_doc_date ='{attrs_sale_doc_date}',
        attrs_cad_cost ='{attrs_cad_cost}',
        attrs_cad_unit ='{attrs_cad_unit}',
        attrs_sale_dep ='{attrs_sale_dep}',
        attrs_children ='{attrs_children}',
        attrs_parcel_type ='{attrs_parcel_type}',
        attrs_sale_doc_num ='{attrs_sale_doc_num}',
        attrs_sale_doc_type ='{attrs_sale_doc_type}',
        attrs_util_by_doc ='{attrs_util_by_doc}'
        where attrs_cn='{attrs_cn}';''')


    try:
        cursor.execute(command)
    except Exception as e:
        print("Object: " +  attrs_cn + " error:" + str(e)) 

    cursor.close()


def db_disconnect(con):
    con.commit()
    con.close()
