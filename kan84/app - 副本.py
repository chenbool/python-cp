#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup as bs
from urllib import request
import re
from time import strftime, time, sleep

__author__ = 'bool'

class App(object):
    soup = ''
    host = "http://www.kan84.net"
    page = [0, 0]
    prev_page = host
    next_page = host
    # init
    def __init__(self):
        pass

    # 获取内容
    def setUrl(self, url):
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        # req = request.Request(url, headers=headers)
        # resp = request.urlopen(req).read().decode("utf-8")
        
        resp = request.urlopen(url).read().decode("gbk")
        self.soup = bs(resp, "html.parser")
        self.getList()

    # 获取电影框列表
    def getList(self):
        res = self.soup.find("div", {"id": "listBox"})
        page = res.find("div", {"id": "tpage"}).find("label").getText()

        # 页数 [ 当前页,总页数 ]
        self.page = re.findall(r"\d{1,}", page)
        # 上一页
        self.prev_page += res.find("div", {"id": "tpage"}).findAll("a", {"class": "prev"})[0]['href']
        # 下一页
        self.next_page += res.find("div", {"id": "tpage"}).findAll("a", {"class": "next"})[0]['href']

        # 获取列表内容
        content = self.soup.find("ul", {"id": "contents"}).findAll("li")
        self.listToDict(content)

    # 把列表转为dict保存
    def listToDict(self, content):

        # 临时保存
        tepList = []

        # 遍历数据
        for item in content:
            temp = {
                'title': item.find("a").find("img")['alt'],
                'logo': item.find("a").find("img")['src'],
                'urls': self.host + item.find("a")['href'],
                'actor': re.sub(".+[：|:]", "", item.find("p", {"class": "actor"}).getText()),
                # 'actor': re.sub(".+[：|:]", "", item.find("p", {"class": "actor"}).getText()).split(","),
                'area': re.sub(".+[：|:]", "", item.find("p", {"class": "type"}).getText()),
                'plot': re.sub(".+[：|:]", "", item.find("p", {"class": "plot"}).getText()),
                'upTime': time(),
                'upDate': strftime("%Y-%m-%d %H:%M:%S")
            }
            tepList.append(temp)
            # 插入数据
            # self.insertData(temp)

        # print(tepList)
        print( "第["+self.page[0]+"]页----->采集完毕\n\n" )

    def insertData(self, temp):
        # sqls = "SELECT * FROM main WHERE urls = '"+temp['urls']+"'"
        # db = Db()
        # findRes = db.dml(sqls)
        # if findRes:
        #     print( findRes[0][1]+"----->已经存在" )
        # else:
        #     sqls = "insert into main ('title','logo','urls','actor','area','plot','upTime','upDate') values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
        #     temp['title'], temp['logo'], temp['urls'], temp['actor'], temp['area'], temp['plot'], temp['upTime'],
        #     temp['upDate'])
        #     db = Db()
        #     if db.ddl(sqls) > 0:
        #         print(temp['title']+'----->采集成功')
        # sleep(0.5)


if __name__ == '__main__':
    api = App()
    api.setUrl('http://www.kan84.net/vod/newscary.html')
    # print(api.page)
    start = int(api.page[0])+1
    end = int(api.page[1])
    # print(api.next_page)
    for key in range(27, end):
        api.setUrl('http://www.kan84.net/vod/newscary'+str(key)+'.html')

    # api.setUrl(api.next_page)
    # print(api.page)
    # print(api.next_page)


