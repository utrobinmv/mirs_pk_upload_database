# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:05:59 2020

@author: denis
"""

from aiohttp import ClientSession, TCPConnector
import asyncio
import os
import datetime
from fake_useragent import UserAgent
from urllib.parse import urlparse, quote
import random

import requests
from bs4 import BeautifulSoup
import socks
import socket
import time
import json
from PIL import Image, ImageOps, ImageChops
import cv2

PATH_result = 'data/'

PATH_output = 'output/'

limit = 2

class TaskPool(object):

    def __init__(self, workers):
        self._semaphore = asyncio.Semaphore(workers)
        self._tasks = set()

    async def put(self, coro):
        await self._semaphore.acquire()

        task = asyncio.ensure_future(coro)
        self._tasks.add(task)
        task.add_done_callback(self._on_task_done)

    def _on_task_done(self, task):
        self._tasks.remove(task)
        self._semaphore.release()

    async def join(self):
        await asyncio.gather(*self._tasks)

    async def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc, tb):
        return self.join()

def bstr(s):
    bs=str(' '.join(s.split()))
    bs=str(bs.replace(":", "_"))
    return (bs)


def remove_zero(text):
    blocks = text.split(':')
    
    for i, block in enumerate(blocks):
        blocks[i] = block.lstrip('0') if block != '0000000' else '0'
    return ':'.join(blocks)


def create_coordinate(xmin, ymin, xmax, ymax):
    xmin = int(xmin)
    ymin = int(ymin)
    xmax = int(xmax)
    ymax = int(ymax)
    

    xdelta = xmax-xmin
    ydelta = ymax-ymin   
    

    if xdelta > ydelta:
        
        if xdelta < 1500:
            xmin = xmin-750
            xmax = xmin + 1500
            ymin = ymin-750
            ymax = ymin + 1500
        
        else:
            xmin = xmin
            xmax = xmax
            ymin = ymin - (xdelta/2)
            ymax = ymin + xdelta
            
            
    else:
        if ydelta < 1500:
            xmin = xmin-750
            xmax = xmin + 1500
            ymin = ymin-750
            ymax = ymin + 1500
        
        else:
            xmin = xmin -(xdelta/2)
            xmax = xmin + xdelta 
            ymin = ymin
            ymax = ymax       
    

    str_coordinate = str(xmin) + ',' + str(ymin) + ',' + str(xmax) + ',' + str(ymax)
    
    return str_coordinate


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    
def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    return most_frequent_pixel    
 
def NDVI_calc(PATH_input):
    bandNIR = cv2.imread(PATH_input + '\\' + 'B08_cut.png')
    bandRed = cv2.imread(PATH_input + '\\' + 'B04_cut.png')    
    
    ndvi = (bandNIR.astype(float)-bandRed.astype(float))/(bandNIR.astype(float)+bandRed.astype(float))

    return ndvi.mean()    

async def fetch(data_field, session):
    os.mkdir(PATH_output + bstr(data_field[0]))
    
    coord = create_coordinate(data_field[1]['xmin'], data_field[1]['ymin'], data_field[1]['xmax'], data_field[1]['ymax'])

    
    status_code = 0
    while status_code != 200:
        try:
            async with session.get('https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/export?layers=show%3A30%2C21%2C17%2C8%2C0&dpi=96&format=PNG32&bboxSR=102100&imageSR=102100&size=1024%2C1024&transparent=true&f=image&bbox=' + coord) as response: 
                status_code = response.status
                body = await response.read()
                with open(PATH_output + bstr(data_field[0]) + "\\sat.png", "wb") as file:
                    file.write(body)                
                await asyncio.sleep(1)
        except:
            pass
    
    cn = remove_zero(data_field[0])
    block = '{"6":"ID = \'' + str (cn) + '\'","7":"ID = \'' + str (cn) + '\'","8":"ID = \'' + str (cn) + '\'","9":"ID = \'' + str (cn) + '\'"}'
    block_encode = quote(block.encode('utf8'))
    
    status_code = 0
    while status_code != 200:
        try:
            async with session.get('https://pkk.rosreestr.ru/arcgis/rest/services/PKK6/CadastreSelected/MapServer/export?bbox=' + coord + '&bboxSR=102100&imageSR=102100&size=1024,1024&dpi=96&format=png32&transparent=true&layers=show:6,7,8,9&f=image&layerDefs=' + block_encode)  as response:  
                status_code = response.status
                body = await response.read()
                with open(PATH_output + bstr(data_field[0]) + "\\mask.png", "wb") as file:
                    file.write(body)                
                await asyncio.sleep(1)
        except:
            pass

    status_code = 0
    while status_code != 200:
        try:
            async with session.get('http://services.sentinel-hub.com/ogc/wms/07d49627-43f7-4af5-9642-595928d2c181?REQUEST=GetMap&BBOX=' + coord + '&LAYERS=B04&MAXCC=20&WIDTH=1024&HEIGHT=1024&FORMAT=image/jpeg') as response: 
                status_code = response.status
                body = await response.read()
                with open(PATH_output + bstr(data_field[0]) + "\\B04.png", "wb") as file:
                    file.write(body)                
                await asyncio.sleep(1)
        except:
            pass

    status_code = 0
    while status_code != 200:
        try:
            async with session.get('http://services.sentinel-hub.com/ogc/wms/07d49627-43f7-4af5-9642-595928d2c181?REQUEST=GetMap&BBOX=' + coord + '&LAYERS=B08&MAXCC=20&WIDTH=1024&HEIGHT=1024&FORMAT=image/jpeg') as response: 
                status_code = response.status
                body = await response.read()
                with open(PATH_output + bstr(data_field[0]) + "\\B08.png", "wb") as file:
                    file.write(body)                
                await asyncio.sleep(1)
        except:
            pass        

    status_code = 0
    while status_code != 200:
        try:
            async with session.get('http://services.sentinel-hub.com/ogc/wms/07d49627-43f7-4af5-9642-595928d2c181?REQUEST=GetMap&BBOX=' + coord + '&LAYERS=NDVI&MAXCC=20&WIDTH=1024&HEIGHT=1024&FORMAT=image/jpeg') as response: 
                status_code = response.status
                body = await response.read()
                with open(PATH_output + bstr(data_field[0]) + "\\NDVI.png", "wb") as file:
                    file.write(body)                
                await asyncio.sleep(1)
        except:
            pass
        
        
        
        
    try:
        mask = Image.open(PATH_output + bstr(data_field[0]) + '\\' + 'mask.png').convert('L')
        mask = ImageOps.invert(mask.point(lambda x: x < 10 and 255))
        img = Image.open(PATH_output + bstr(data_field[0]) + '\\' + 'sat.png')
        img.putalpha(mask)
        img = trim(img)
        img.save(PATH_output + bstr(data_field[0]) + '\\' +  'rr_cut.png')
 
       
        img = Image.open(PATH_output + bstr(data_field[0]) + '\\' + 'B04.png')
        img.putalpha(mask)
        img = trim(img)
        img.save(PATH_output + bstr(data_field[0]) + '\\' +  'B04_cut.png')        

        
        img = Image.open(PATH_output + bstr(data_field[0]) + '\\' + 'B08.png')
        img.putalpha(mask)
        img = trim(img)
        img.save(PATH_output + bstr(data_field[0]) + '\\' +  'B08_cut.png')

        img = Image.open(PATH_output + bstr(data_field[0]) + '\\' + 'NDVI.png')
        img.putalpha(mask)
        img = trim(img)
        img.save(PATH_output + bstr(data_field[0]) + '\\' +  'NDVI_cut.png')

    except:
        pass
    
    ndvi = NDVI_calc(PATH_output + bstr(data_field[0]))
    with open(PATH_output + bstr(data_field[0]) + "\\NDVI.txt", "w") as file_ndvi:
        file_ndvi.write(str({'data_field[0]':ndvi}))


def add_objects():

    with open(PATH_result + 'result.json', 'r') as f:    
        file_data = json.loads(json.loads(json.dumps(f.read())))
    
    data_list = []
    for k, v in file_data.items():
        data_list.append([k,v])
        
    loop.create_task(_main(data_list[:2]))

# def add_object(v):

#     data_list = []
#     data_list.append([0,v])
        
#     loop.create_task(_main(data_list[:2]))


async def _main(urls):
    connector = TCPConnector(limit=None)
    total_requests = len(urls)
    async with ClientSession(connector=connector, headers={'User-Agent': UserAgent().random}) as session, TaskPool(limit) as tasks:
        for i in range(total_requests):
            await tasks.put(fetch(urls[i], session))
    print('Done')



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_objects()) 