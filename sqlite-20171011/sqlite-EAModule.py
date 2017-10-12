#coding=utf-8

import requests
import time
import datetime
import sqlite3
import re, os

FX678_XAG_URL = 'http://api.q.fx678.com/quotes.php?exchName=WGJS&symbol=XAG'
QUOTATION_STRUCTURE = ('startPrice','realPrice','maxPrice','minPrice','time')

QUOTATION_DB_CREATE = '''create table quotation(
    id integer primary key autoincrement not null default 1,
    startPrice   float,
    realPrice    float,
    maxPrice     float,
    minPrice     float,
    time         float);'''

QUOTATION_DB_INSERT = 'insert into quotation (startPrice,realPrice,maxPrice,minPrice,time)\
    values(?, ?, ?, ?, ?)'

def queryInfo(url):
    '''获取并提取信息'''
    try:
        r = requests.get(url)
        content = r.text.split('{')[1].split('}')[0].split(',')
        print content
        tag = []
        value = []

        for item in content:
            tag.append(item.split(':')[0])
            value.append(item.split(':')[1].strip('[""]'))

        infoDict = dict(zip(tag,value))
        print infoDict
    except (Exception),e:
        print "Exception: "+e.message

    return [infoDict[u'"p"'],infoDict[u'"b"'],infoDict[u'"h"'],infoDict[u'"l"'],\
         time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(infoDict[u'"t"'])))]

def create_file_name_prefix():
    """ build database prefix"""
    dt = datetime.datetime.now()
    year,week = dt.strftime('%Y'),dt.strftime('%U')

    fileNamePrefix = folderName = year+'-'+week

    if not os.path.exists(folderName):
        # 创建当周数据库文件夹
        os.makedirs(folderName)

    return fileNamePrefix

def db_quotation(prefix, priceList):
    '''行情数据库操作'''
    file = prefix+'/'+prefix+'.db'
    isExist = os.path.exists(file)

    db = sqlite3.connect(file)
    dbCursor = db.cursor()
    #First: create db if empty
    if not isExist:
        try:
            dbCursor.execute(QUOTATION_DB_CREATE)
        except (Exception),e:
            print "Exception: "+e.message

    #Second: insert some information
    try:
        db.execute(QUOTATION_DB_INSERT,priceList)
    except (Exception),e:
        print "Exception: "+e.message

    db.commit()
    dbCursor.close()
    db.close()

def db_earnRate(prefix):
    '''盈利胜率数据库操作'''

def main():
    '''main routine'''
    priceList = queryInfo(FX678_XAG_URL)
    print priceList

    fileNamePrefix = create_file_name_prefix()
    db_quotation(fileNamePrefix, priceList)

if __name__ == '__main__':
    main()