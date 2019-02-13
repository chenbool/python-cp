#!/usr/bin/python
# -*- coding: utf-8 -*-
import records
import time
import requests
from lxml import html
from gevent import monkey
import gevent
# gevent.monkey.patch_all()

class Train(object):
    baseUrl = 'https://kjh.55128.cn'
    db = ''
    def __init__(self,):
        # 关闭https证书验证警告
        requests.packages.urllib3.disable_warnings()
        self.db = records.Database('mysql://root:root@localhost/db?charset=utf8')
        # self.db = records.Database('sqlite:///data.db')

    # 返回查询结果
    def run(self):
        tree = self.get_content('/k/index.html')
        # 标题
        #cp_title = tree.xpath('//div[@class="cp-fl-title"]/text()')
        #列表名称
        # cp_list = tree.xpath('//a[@class="lot-list"]/text()')
        # 列表网址
        cp_list = tree.xpath('//a[@class="lot-list"]/@href')

        # gevent.joinall([gevent.spawn(self.get_content, '/k/index.html')])
        temp = []
        # 遍历
        for item in cp_list:
            # print(self.baseUrl+item)
            # self.get_info(item)
            temp.append(gevent.spawn(self.get_info, item))

        # 开启协程
        gevent.joinall(temp)

    # 获取详情页
    def get_info(self, url):
        tree = self.get_content(url)
        # //*[@id="kj"]/div[2]/div
        # 名称
        kaij_name = tree.xpath('//*[@id="kj"]/div[2]/div/div[@class="kaij-title"]/span[@class="kaij-name"]/text()')
        # 期号
        kaij_qs = tree.xpath('//*[@id="kj"]/div[2]/div/div[@class="kaij-title"]/span[@class="kaij-qs"]/text()')
        # 开奖号码
        kaij_code = tree.xpath('//*[@id="kj"]/div[2]/div/div[@class="kaij-cartoon"]/span/text()')

        # 下一期
        kaij_qs_next = tree.xpath('//*[@id="kj"]/div[3]/div[1]/div[@class="line"]/span[@class="kaij-qsnext"]/text()')

        # 开奖描述 //*[@id="kj"]/div[3]/div[2]/div
        kaij_desc = tree.xpath('//*[@id="kj"]/div[3]/div[2]/div[@class="kaij-list"]/text()')
        # 开奖数据
        data = {
            'name': kaij_name[0].strip(),
            'expect': kaij_qs[0].strip(),
            'opencode': ','.join(kaij_code),
            'expect_next': kaij_qs_next[0].strip(),
            'desc': kaij_desc[1].strip(),
            'opentime': time.time(),
            'opendate': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        }
        print(data)
        # 插入数据库
        # INSERT INTO `data` (`name`, `expect`, `opencode`, `expect_next`, `desc`, `opentime`, `opendate`) VALUES ('1', '1', NULL, '1', NULL, NULL, NULL);
        sql = "INSERT INTO `data` (`name`, `expect`, `opencode`, `expect_next`, `desc`, `opentime`, `opendate`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(
            data['name'], data['expect'], data['opencode'], data['expect_next'], data['desc'], data['opentime'], data['opendate']
        )
        self.db.query(sql)
        print(data['name']+':添加成功')
        exit()


    # 获取内容
    def get_content(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        proxies = {
            'http': 'http://183.148.148.81:9999',
            'http': 'http://121.61.2.56:9999',
            # 'https': 'https://112.98.126.98:37614'
        }
        page = requests.get(self.baseUrl+url, headers=headers, proxies=proxies)
        # page = page.text.strip();
        tree = page.text.replace('\r\n', '')  # 替换成空格
        return html.fromstring(tree)

def main():
    train = Train()
    train.run()
    
if __name__ == "__main__":
    main()
