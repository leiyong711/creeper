# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: 垃圾测试
# author: "Lei Yong" 
# creation time: 2017/6/15 0015 14:22
# Email: leiyong711@163.com

import re
import datetime
import time
import urllib  # 网络访问模块
import MySQLdb  # 数据库模块

start = datetime.datetime.now()  # 开始计时


# 数据库
class sql:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='',
            db='test',
            charset='utf8',
        )  # 连接数据库

    # 插入目录到数据库
    def addNovels(self, sort, nmae, imgurl, description, stat, author):
        cur = self.conn.cursor()
        cur.execute(
            "insert into novel(sort,nmae,imgurl,description,state,author) values(%s,'%s','%s','%s','%s','%s') " % (
            sort, nmae, imgurl, description, stat, author))
        lastrowid = cur.lastrowid  # 获取当前插入的id
        cur.close()
        self.conn.commit()
        return lastrowid

    # 插入章节到数据库
    def addChapters(self, novelid, title, content):
        cur = self.conn.cursor()
        cur.execute("insert into chapter(novelid,title,content) values(%s,'%s','%s')" % (novelid, title, content))
        cur.close()
        self.conn.commit()


domin = 'http://www.quanshuwang.com'  # 全书网首页url


# 获取地图目录
def getSortList(sort):
    res = urllib.urlopen('%s/map/%s.html' % (domin, sort))
    html = res.read().decode('gbk')  # 获取请求的html源代码
    reg = r'<a href="(/book/.+?)" target="_blank">(.+?)</a>'  # 正则
    return re.findall(reg, html)


# 获取目录
def getNovelList(url):
    html = urllib.urlopen(url).read().decode('gbk')
    reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    return re.findall(reg, html)


# 获取章节
def getChapterContent(url):
    html = urllib.urlopen(url).read().decode('gbk')
    reg = r'style5\(\);</script>(.*?)<script type="text/javascript">'
    return re.findall(reg, html)[0]


mysql = sql()  # 实例类

for sort in range(1, 10):
    for novel in getSortList(sort):  # 遍历所有小说目录
        lastrowid = mysql.addNovels(sort, novel[1], 'img', 'des', 'sta', 'au')
        print u'正在保存《%s》到数据库' % novel[1]
        for chapter in getNovelList(domin + novel[0]):  # 遍历所有小说章节
            # print chapter[0], chapter[1]
            url = domin + novel[0].replace('index.html', chapter[0])
            content = getChapterContent(url)
            mysql.addChapters(lastrowid, chapter[1], content)
            print u'正在保存  %s  章节到数据库' % chapter[1]
            # break
            # break

# 统计耗时
end = datetime.datetime.now()
output = open('time.txt', 'a')
output.write('\n------------------------------------- %s -----------------------------------------\n 开始时间：%s'
             '\n 结束时间：%s\n ' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), start, end))
output.write('耗时：' + str(end - start) + '\n')
output.close()
