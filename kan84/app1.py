#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re
import time
import json
import dataset
import requests
from bs4 import BeautifulSoup

class App(object):

    baseUrl = 'http://www.kan84.net'
    db = ''

    def __init__(self):
        # 关闭https证书验证警告
        requests.packages.urllib3.disable_warnings()
        self.db = dataset.connect('mysql://root:root@127.0.0.1/db?charset=utf8')

    def run(self, url):
        soup = response = self.get_content(url)

        # 页数的文本
        page = soup.find("div", {"class": "pages"}).label.get_text()
        # 页数 [ 当前页,总页数 ]
        page = re.findall(r"\d{1,}", page)
        start_page = int(page[0]) + 1
        end_page = int(page[1])

        # 获取页面列表
        self.get_page_list(url)

        # start_page = 20

        # 遍历页数
        for key in range(start_page, end_page):
            url = '/vod/newscary' + str(key) + '.html'
            self.get_page_list(url)
            print("第" + str(key) + "页 --> 采集完成")

    # 获取页面的列表
    def get_page_list(self, url):
        # bs
        soup = self.get_content(url)
        # lists
        lists = soup.find("div", {"id": "listBox"}).find("ul", {"id": "contents"}).find_all("li")
        # 遍历获取详情
        for item in lists:
            self.get_info(item)

    # 获取详情介绍
    def get_info(self, data):
        url = data.a.get("href")
        # actor
        k_actor = data.find("p", {"class": "actor"})
        k_actor = k_actor.get_text().replace(k_actor.em.get_text(), "").strip()
        # type
        k_type = data.find("p", {"class": "type"})
        k_type = k_type.get_text().replace(k_type.em.get_text(), "")
        # plot
        k_plot = data.find("p", {"class": "plot"})
        k_plot = k_plot.get_text().replace(k_plot.em.get_text(), "")

        temp = {
            "url": url,
            "logo": data.a.img.get("src"),
            "title": data.a.img.get("alt"),
            "actor": k_actor,
            "region": k_type,
            "plot": k_plot
        }

        # 进入详情页
        soup = self.get_content(url)
        # 获取信息
        info = soup.find("div", {"class": "info"}).find_all("dl")
        temp["status"] = info[1].dd.span.get_text()
        try:
            temp["director"] = info[2].dd.a.get_text()
        except:
            temp["director"] = "暂无"
        temp["level"] = info[4].dd.span.get_text()
        temp["date"] = info[6].dd.span.get_text()
        temp["year"] = info[7].dd.span.get_text()
        temp["alias"] = info[8].dd.span.get_text()
        # jq-list
        temp["desc"] = soup.find("ul", {"class": "jq-list"}).get_text().strip()

        # 操作数据库
        table = self.db['kan']
        res = table.find_one(title=temp['title'])
        if res is None:
            id = table.insert(temp)
            print("[main]"+str(id)+"--"+temp['title']+" -->插入成功")
        else:
            # id = res["id"]
            print(temp['title']+" --> 已经存在")
            return

        # liebiao
        liebiao = soup.find("div", {"id": "liebiao"}).find_all("ul", {"class": "downurl"})
        # 遍历页数 记录下载地址
        for key in range(0, len(liebiao)):
            li_list = liebiao[key].find_all("li")
            res = self.get_downurl(li_list)
            # 把数据插入到数据库
            table = self.db['kan_list']
            id = table.insert({
                "pid": id,
                "content": json.dumps(res)
            })
            # print("[list]"+str(id)+" -->插入成功")

    # 获取下载地址 或者章节
    def get_downurl(self, data):
        temp = []
        for item in data:
            temp.append({
                "title": item.a.get("title"),
                "url": item.a.get("href"),
            })
        return temp

    # 获取网页内容
    def get_content(self, url):
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gb2312, utf-8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"
        }
        proxies = {
            # 'https': 'http://112.87.69.158:9999',
        }
        try:
            page = requests.get(self.baseUrl+url, headers=headers, proxies=proxies, timeout=(10, 8))
            res = page.text.encode(page.encoding).decode('gbk')
            soup = BeautifulSoup(res, features="lxml")
            return soup
        except requests.exceptions.HTTPError:
            print('状态异常: ' + self.baseUrl + url)
        except requests.exceptions.ConnectionError:
            print('连接异常: '+self.baseUrl+url)
        except requests.exceptions.InvalidURL:
            print('网址错误: ' + self.baseUrl + url)
        except requests.exceptions.ConnectTimeout:
            print('链接超时: '+self.baseUrl+url)
        except requests.exceptions.InvalidHeader:
            print('请求头异常: '+self.baseUrl+url)
        except requests.exceptions.UnrewindableBodyError:
            print('页面异常: '+self.baseUrl+url)
        except:
            print('运行异常: '+self.baseUrl+url)

if __name__ == '__main__':
    start = time.time()

    app = App()

    app.run('/vod/newscary.html')

    # 计算执行时间
    end = time.time()
    print('执行时间: %f 秒' %(end-start))



