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
    baseUrl = 'https://www.feixiaohao.com'
    db = ''
    def __init__(self,):
        # 关闭https证书验证警告
        requests.packages.urllib3.disable_warnings()
        self.db = records.Database('mysql://root:root@localhost/db?charset=utf8')

    # 返回查询结果
    def run(self):
        jsonList = self.get_content('https://dncapi.feixiaohao.com/api/coin/data_list?webp=1', True)

        temp = []
        # 遍历
        for item in jsonList['data']:
            temp.append(gevent.spawn(self.get_info, item))
            # self.get_info(item)

        # 开启协程
        gevent.joinall(temp)

    # 获取详情页
    def get_info(self, data):
        tree = self.get_content('/currencies/'+data['code'])
        try:
            # 当前价格
            hb_current = tree.xpath(
                '//*[@id="__layout"]/section/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/span/span/text()')
            # 当前汇率
            hb_diff = tree.xpath(
                '//*[@id="__layout"]/section/div/div/div[1]/div[1]/div[2]/div[1]/div[3]/span[1]/text()')
            # 最高
            hb_high = tree.xpath(
                '//*[@id="__layout"]/section/div/div/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/span/text()')
            # 最低
            hb_low = tree.xpath(
                '//*[@id="__layout"]/section/div/div/div[1]/div[1]/div[2]/div[1]/div[4]/div[2]/span/text()')

            # 存入到dict
            data['current'] = hb_current[0].strip()
            data['diff'] = hb_diff[0].replace('+', '')
            data['high'] = hb_high[0].replace('¥', '')
            data['low'] = hb_low[0].replace('¥', '')
            data['opentime'] = time.time()
            data['opendate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(data)
            self.insert_db(data)
        except:
            print('采集异常: /currencies/'+data['code'])


    # 插入数据库
    def insert_db(self, data):
        # INSERT INTO `db`.`main` (`code`, `name`, `name_zh`, `symbol`, `type`, `logo`, `current`, `diff`, `high`, `low`, `opentime`, `opendate`) VALUES ( NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
        sql = "INSERT INTO `main` (`code`, `name`, `name_zh`, `symbol`, `type`, `logo`, `current`, `diff`, `high`, `low`, `opentime`, `opendate`) VALUES ( '%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(
            data['code'], data['name'], data['name_zh'], data['symbol'], data['type'], data['logo'], data['current'], data['diff'], data['high'], data['low'], data['opentime'],data['opendate'],
        )
        self.db.query(sql)
        print(data['name_zh']+': ￥'+data['current']+'   -> 添加成功')

    # 获取内容
    def get_content(self, url, jsonList = False):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        proxies = {
            'http': 'http://183.148.148.81:9999',
            'http': 'http://121.61.2.56:9999',
        }
        try:
            # 判断是否获取 json
            if jsonList:
                page = requests.get(url, headers=headers, proxies=proxies, timeout=(10, 5))
                return page.json()
            else:
                page = requests.get(self.baseUrl+url, headers=headers, proxies=proxies, timeout=(10, 8))
                tree = page.text.replace('\r\n', '')  # 替换成空格
                # print(tree)
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
        except requests.exceptions.ChunkedEncodingError:
            print('编码异常: '+self.baseUrl+url)
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
