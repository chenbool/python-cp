#!/usr/bin/python3
# -*- coding:utf-8 -*-

import gevent
from gevent import monkey
monkey.patch_all()

import re
import time
import records
import requests
from lxml import html

class App(object):

    baseUrl = 'http://www.kan84.net'
    db = ''

    def __init__(self):
        # 关闭https证书验证警告
        requests.packages.urllib3.disable_warnings()
        self.db = records.Database('mysql://root:root@localhost/db?charset=utf8')

    def run(self, url):
        tree = self.get_content(url)
        # 获取最后一页
        last_page_res = tree.xpath('//*[@id="tpage"]/label/text()')
        # 页数 [ 当前页,总页数 ]
        page = re.findall(r"\d{1,}", last_page_res[0])
        # print(page)
        start = int(page[0])+1
        end = int(page[1])

        # gevent
        temp = [gevent.spawn(self.get_page, '/vod/newscary.html')]
        # 遍历页数
        for key in range(start, end):
            urls = '/vod/newscary' + str(key) + '.html'
            # self.get_page(urls)
            temp.append(gevent.spawn(self.get_page, urls))
            # print('第'+str(key)+'页-->采集完成')

        # 开启协程
        gevent.joinall(temp)

    # 获取页面的列表
    def get_page(self, url):
        tree = self.get_content(url)
        # 获取列表
        lists = tree.xpath('//*[@id="contents"]/li/a/@href')
        # 遍历获取详情
        for item in lists:
            self.get_info(item)

    # 获取详情介绍
    def get_info(self, url):
        tree = self.get_content(url)
        # 获取logo
        kan_logo = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[1]/img/@src')
        # 标题
        kan_title = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[2]/h2/text()')
        # 主演
        kan_star = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[3]/div/dl[1]/dd/a/text()')
        kan_star = ",".join(kan_star)
        # 状态
        kan_status = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[3]/div/dl[2]/dd/span/text()')
        # 导演
        kan_director = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[3]/div/dl[3]/dd/a[1]/text()')
        # 地区
        kan_region = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[3]/div/dl[4]/dd/text()')
        # 星级
        kan_level = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[3]/div/dl[5]/dd/span/text()')
        # 上映时间
        kan_time = tree.xpath('//*[@id="addtime"]/text()')
        # 年份
        kan_year = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[3]/div/dl[8]/dd/span/text()')
        # 别名
        kan_alias = tree.xpath('//*[@id="detail-box"]/div[1]/div/div[3]/div/dl[9]/dd/span/text()')
        # 描述
        kan_desc = tree.xpath('//*[@id="latest-focus"]/div/ul/text()')

        # 信息存入 dict
        temp = {
            'logo': kan_logo[0],
            'title': kan_title[0],
            'star': kan_star,
            'status': kan_status[0],
            'director': kan_director[0],
            'region': kan_region[0],
            'level': kan_level[0],
            'date': kan_time[0],
            'year': kan_year[0],
            'alias': kan_title[0],
            # 'alias': kan_alias[0],
            'desc': kan_desc[0],
            'url': self.baseUrl+url
        }
        # 插入数据库
        self.insert_db(temp)

    # 插入数据库
    def insert_db(self, data):
        sql = "SELECT * FROM `kan` WHERE `title`='%s'  AND `director`= '%s'" %(data['title'], data['director'])
        # print(sql)
        rows = self.db.query(sql)
        # 检测是否存在
        # if rows is None:
        if rows is None:
            # INSERT INTO `kan` (`logo`, `title`, `star`, `status`, `director`, `region`, `level`, `date`, `year`, `alias`, `desc`, `url`) VALUES ( '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2');
            sql = "INSERT INTO `kan` (`logo`, `title`, `star`, `status`, `director`, `region`, `level`, `date`, `year`, `alias`, `desc`, `url`) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(
                data['logo'], data['title'], data['star'], data['status'], data['director'], data['region'], data['level'], data['date'], data['year'], data['alias'], data['desc'], data['url']
            )
            self.db.query(sql)
            print(data['title']+': '+data['region']+' -> 添加成功')
        else:
            print(data['title'] + ': '+data['region']+' -> 已经存在')

    # 获取内容
    def get_content(self, url):
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
        proxies = {
            'https': 'http://112.87.69.158:9999',
        }
        try:
            page = requests.get(self.baseUrl+url, headers=headers, proxies=proxies, timeout=(10, 8))
            # print(page.text.encode(page.encoding).decode('gbk'))
            res = page.text.encode(page.encoding).decode('gbk')
            return html.fromstring(res)
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
        except requests.exceptions.ChunkedEncodingError:
            print('编码异常: '+self.baseUrl+url)
        except:
            print('运行异常: '+self.baseUrl+url)

if __name__ == '__main__':
    start = time.time()

    train = App()
    train.run('/vod/newscary.html')

    # 计算执行时间
    end = time.time()
    print('执行时间: %f 秒' %(end-start))



