#!/usr/bin/python
# -*- coding: utf-8 -*-
import gevent
from gevent import monkey
monkey.patch_all()
import records
import time
import requests
from lxml import html

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

        # cp_list = ['/k/kjls/dfc-gxklsc.html']

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
        # print(data)
        self.insert_db(data)

    # 插入数据库
    def insert_db(self, data):
        sql = "SELECT * FROM `data` WHERE `name` = '%s'  AND expect = %s " %(data['name'],data['expect'])
        rows = self.db.query(sql)
        # 检测是否存在
        if rows is None:
            sql = "INSERT INTO `data` (`name`, `expect`, `opencode`, `expect_next`, `desc`, `opentime`, `opendate`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(
                data['name'], data['expect'], data['opencode'], data['expect_next'], data['desc'], data['opentime'], data['opendate']
            )
            self.db.query(sql)
            print(data['name']+': 第'+data['expect']+'期  开奖号码: '+data['opencode']+'  -> 添加成功')
        else:
            print(data['name'] + ': 第' + data['expect'] + '期  开奖号码: ' + data['opencode'] + '  -> 已经存在')


    # 获取内容
    def get_content(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        proxies = {
            'http': 'http://121.61.2.56:9999',
            'http': 'http://116.208.55.173:9999'
        }
        try:
            # timeout=([连接超时时间], [读取超时时间])
            page = requests.get(self.baseUrl+url, headers=headers, proxies=proxies, timeout=(10, 5))
            tree = page.text.replace('\r\n', '')  # 替换成空格
            return html.fromstring(tree)
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

def main():
    start = time.time()

    train = Train()
    train.run()

    # 计算执行时间
    end = time.time()
    print('执行时间: %f 秒' %(end-start))
    
if __name__ == "__main__":
    main()
