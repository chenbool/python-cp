#!/usr/bin/python
# -*- coding: utf-8 -*-

import gevent
from gevent import monkey
monkey.patch_all()

import re
import os
import time
import execjs
import dataset
import requests
from bs4 import BeautifulSoup

class App(object):

    db = None
    req = None
    cookie = None
    headers = None
    img_header = None
    baseDir = "mh/"
    baseUrl = 'http://www.1kkk.com'

    def __init__(self):
        self.req = requests.session()
        self.img_header = {
            'Host': 'manhua1032-101-69-161-98.cdndm5.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'http://www.1kkk.com/ch932-772307/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.req.headers.update(self.img_header)
        self.db = dataset.connect('mysql://root:root@127.0.0.1/mh?charset=utf8')

    def run(self):
        response = self.get_content('/manhua-list-s2/')
        # self.__w('index', response.text)
        self.cookie = response.cookies
        soup = BeautifulSoup(response.text, features="lxml")
        # 获取列表
        group = soup.find("ul", {'class': 'mh-list'}).find_all("li")

        # gevent.joinall([gevent.spawn(self.get_content, '/k/index.html')])
        # 遍历列表
        # temp = []
        for item in group:
            self.get_item(item)
            # temp.append(gevent.spawn(self.get_item, item))

        # 开启协程
        # gevent.joinall(temp)

    # 获取列表
    def get_item(self, data):
        data = data.find("div", {'class': 'mh-item'})
        # logo
        m_logo = data.find("p", {'class': 'mh-cover'}).get("style")
        m_logo = re.findall("http://.+\.[a-z]{3,}", m_logo)[0]

        # mh-item-tip
        m_tip = data.find("div", {'class': 'mh-tip-wrap'}).find("div", {'class': 'mh-item-tip'})
        m_title = m_tip.find("a").get("title")
        m_url = m_tip.find("a").get("href")

        # mh-item-tip-detali
        m_detali = m_tip.find("div", {'class': 'mh-item-tip-detali'})
        m_author = m_detali.find("p", {'class': 'author'}).find("a").get_text()

        # chapter
        m_chapter = m_detali.find("p", {'class': 'chapter'}).find("a")
        m_last_title = re.findall("\d{1,}", m_chapter.get_text())[0]
        m_last_url = m_chapter.get("href")
        m_desc = m_detali.find("div", {'class': 'desc'}).get_text().strip()

        # 定义dict
        item = {
            "title": m_title,
            "logo": m_logo,
            "author": m_author,
            "url": m_url,
            "desc": m_desc,
            "last_title": m_last_title,
            "last_url": m_last_url,
        }

        # 进入漫画详情页
        self.get_detali(item)

    # 漫画简介详情页
    def get_detali(self, data):
        response = self.get_content(data["url"])
        cookie = response.cookies
        soup = BeautifulSoup(response.text, features="lxml")
        # m_tip
        m_tip = soup.find("p", {'class': 'tip'}).find_all("span", {'class': 'block'})
        data["status"] = m_tip[0].span.get_text()
        try:
            data["type"] = m_tip[1].span.get_text()
        except:
            data["type"] = ""

            #  tempc
        m_list = soup.find("div", {'id': 'chapterlistload'}).find_all("li")
        dir_name = self.baseDir+re.findall("\d{1,}", data['url'])[0]+"/"
        data["count"] = len(m_list)

        # 操作数据库
        table = self.db['m_data']
        res = table.find_one(title=data['title'])
        # 检测数据库是否有数据
        if res is None:
            # 插入sql
            id = table.insert(dict(data))
        else:
            id = res["id"]
            data["id"] = res["id"]
            table.update(data, ['id'])

            # 检测目录是否存在
        if os.path.exists(dir_name) == False:
            os.mkdir(dir_name)
        else:
            dirs = os.listdir(dir_name)
            if len(dirs) == len(m_list):
                print("此漫画已经存在")
                return
            else:
                print("此漫画缺少部分章节")

        # 遍历章节
        for item in m_list:
            self.get_chapter(item, cookie, dir_name, id)
        # print(len(m_list))

    # 获取章节信息
    def get_chapter(self, data, cookie, dir_name, id):
        chapter = data.a
        page_size = chapter.span.get_text()
        m_title = chapter.get_text().replace(page_size, "").strip()
        page_size = re.findall("\d{1,}", page_size)
        if len(page_size) > 0:
            page_size = page_size[0]
        else:
            return
        # m_date = re.findall("\d{4}-\d{2}-\d{2}", m_title)[0]
        # m_title = m_title.replace(m_date, "").strip()

        item = {
            "pid": id,
            "title": m_title,
            "url": chapter.get("href"),
            "size": page_size,
            "chapter": re.findall("\d{1,}", m_title)[0],
            # "date": m_date,
        }
        item["dir"] = dir_name+item["chapter"]
        item["cid"] = item["url"].split('-')[-1][:-1]

        # 操作数据库
        table = self.db['m_data_list']
        res = table.find_one(title=item['title'], pid=id)
        # 检测数据库是否有数据
        if res is None:
            # 插入sql
            table.insert(dict(item))
        else:
            item["id"] = res["id"]
            table.update(item, ['id'])

        # 获取章节
        response = self.get_content(item["url"])
        cid = item["cid"]
        # 获取参数
        parm = self.get_parm(response.text)
        # 遍历获取
        page = 1
        while page <= int(page_size):
            link = "http://www.1kkk.com/ch932-772307/chapterfun.ashx?cid=" + cid + "&page=" + str(page) + "&key=&language=1&gtk=6&_cid=" + cid + "&_mid=" + parm['DM5_MID'] + "&_dt=" + parm['DM5_VIEWSIGN_DT'] + "&_sign=" + parm['DM5_VIEWSIGN']
            link_response = requests.get(link, headers=self.headers, cookies=cookie)
            cookie = link_response.cookies
            try:
                # 获取图片列表
                img_result = execjs.eval(link_response.text)
            except:
                return
            # 遍历下载
            for img in img_result:
                img_response = self.req.get(img, headers=self.img_header)
                if img_response.status_code != 200:
                    print("图片请求出错")
                    exit()

                # 检测目录是否存在
                path = dir_name+item["chapter"]
                # 检测此章节是否下载所有页数
                if os.path.exists(path) == False:
                    os.mkdir(path)
                else:
                    dirs = os.listdir(path)
                    if len(dirs) == int(page_size):
                        print("此章节已经存在")
                        return
                    else:
                        pass
                        # print("此章节缺少部分图片")

                file_path = path+"/"+str(page) + '.jpg'
                # 检测文件是否存在
                if os.path.exists(file_path) == False:
                    f = open(file_path, 'wb')
                    f.write(img_response.content)
                    f.close()
                    print(file_path + '-->[√]保存成功')
                else:
                    print(file_path+'-->[×]已经存在')
                page = int(img.split("_")[0].split("/")[-1]) + 1

    # 获取参数
    def get_parm(self, text):
        parm = {}
        DM5_MID = re.findall(r'var DM5_MID=(.*?);', text)
        if len(DM5_MID) > 0:
            parm['DM5_MID'] = DM5_MID[0]
        else:
            parm['DM5_MID'] = ''
        DM5_VIEWSIGN = re.findall(r'DM5_VIEWSIGN="(.*?)";', text)
        if len(DM5_VIEWSIGN) > 0:
            parm['DM5_VIEWSIGN'] = DM5_VIEWSIGN[0]
        else:
            parm['DM5_VIEWSIGN'] = ''
        DM5_VIEWSIGN_DT = re.findall(r'DM5_VIEWSIGN_DT="(.*?)";', text)
        if len(DM5_VIEWSIGN_DT) > 0:
            parm['DM5_VIEWSIGN_DT'] = DM5_VIEWSIGN_DT[0]
        else:
            parm['DM5_VIEWSIGN_DT'] = ''
        return parm

    # 写出文件
    def __w(self, name, data):
        f = open(name+'.html', 'w', encoding='utf-8')
        f.write(data)
        f.close()

    # 获取内容
    def get_content(self, url):
        self.headers = {
            'Host': 'www.1kkk.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': 'http://www.1kkk.com/ch932-772307/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        proxies = {
            # 'http': 'http://183.148.148.81:9999'
        }
        try:
            return self.req.get(self.baseUrl+url, headers=self.headers, proxies=proxies, timeout=(10, 5))
        except requests.exceptions.HTTPError:
            print('状态码异常: ' + self.baseUrl + url)
        except requests.exceptions.ConnectionError:
            print('连接异常: '+self.baseUrl+url)
        except requests.exceptions.InvalidURL:
            print('网址错误: ' + self.baseUrl + url)
        except requests.exceptions.ConnectTimeout:
            print('连接超时: '+self.baseUrl+url)
        except requests.exceptions.InvalidHeader:
            print('请求头异常: '+self.baseUrl+url)
        except:
            print('请求异常')

def main():
    start = time.time()

    app = App()
    app.run()

    # 计算执行时间
    end = time.time()
    print('执行时间: %f 秒' % (end - start))

if __name__ == "__main__":
    main()

