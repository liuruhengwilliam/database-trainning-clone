#coding=utf-8

import requests
import time
import datetime
import sqlite3
import re, os

FX678_XAG_URL = 'http://api.q.fx678.com/quotes.php?exchName=WGJS&symbol=XAG'
QUOTATION_STRUCTURE = [ 'startPrice','realPrice','maxPrice','minPrice','time']
QUOTATION_DATABASE_STRUCTURE = '''create table quotation(
    startPrice,
    realPrice,
    maxPrice,
    minPrice,
    time
);'''

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
            #value.append(re.sub('\"]', '', re.sub('\["', '', item.split(':')[1])))

        infoDict = dict(zip(tag,value))
        print infoDict
    except (Exception),e:
        print "Exception: "+e.message

    return dict(zip(QUOTATION_STRUCTURE,\
        [infoDict[u'"p"'],infoDict[u'"b"'],infoDict[u'"h"'],infoDict[u'"l"'],\
         time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(infoDict[u'"t"'])))]))

def create_file_name_prefix():
    """ build database prefix"""
    dt = datetime.datetime.now()
    year,week = dt.strftime('%Y'),dt.strftime('%U')

    fileNamePrefix = folderName = year+'-'+week
    #quotation_filename = year+'-'+week+'.db'
    #earnRate_filename = year+'-'+week+'ER'+'.db'
    #print quotation_filename,earnRate_filename

    if not os.path.exists(folderName):
        # 创建当周数据库文件夹
        os.makedirs(folderName)

    return fileNamePrefix

def database_quotation(prefix):
    '''行情数据库操作'''
    file = prefix+'/'+prefix+'.db'

    db = sqlite3.connect(file)
    dbCursor = db.cursor()
    dbCursor.execute(QUOTATION_DATABASE_STRUCTURE)
    dbCursor.close()
    db.close()

def database_earnRate(prefix):
    '''盈利胜率数据库操作'''

def main():
    '''main routine'''
    priceDict = queryInfo(FX678_XAG_URL)
    print priceDict

    fileNamePrefix = create_file_name_prefix()
    database_quotation(fileNamePrefix)

if __name__ == '__main__':
    main()