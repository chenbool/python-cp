
import time
import requests
from lxml import html
from fake_useragent import UserAgent

class App(object):
    # http://n.1whour.com/
    # http://comic.kukudm.com/comiclist/2160/52245/
    # https://www.mkzhan.com
    baseUrl = 'http://comic.kukudm.com'

    def __init__(self):
        # 关闭https证书验证警告
        requests.packages.urllib3.disable_warnings()

    def run(self):
        tree = self.get_content('/')
        kaij_name = tree.xpath('/html/body/table[3]/tbody/tr/td/table/tbody/tr/td/a/@href')
        print(kaij_name)

    # 获取内容
    def get_content(self, url):
        # 随机请求头
        ua = UserAgent()
        headers = {
            "Host": "comic.kukudm.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gb2312, utf-8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "User-Agent": ua.random,
            "Cookie": "__cfduid=d0a6e23cb306995e15247cdb63ce4819d1550113308; UM_distinctid=168e9f40309325-0f2beaa5e1a68f-574e6e46-3d10d-168e9f4030a4da; CNZZDATA1273361586=927471036-1550108352-%7C1550108352",
        }
        proxies = {
            # 'http': 'http://112.85.164.23:9999',
            # 'http': 'http://121.61.0.12:9999',
        }
        try:
            resp = requests.get(self.baseUrl+url, headers=headers,proxies=proxies, timeout=(10, 8))
            if resp.status_code == 200:
                res = resp.text.encode(resp.encoding).decode('gbk')
                return html.fromstring(res)
            else:
                print('状态码错误')
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
    train.run()

    # 计算执行时间
    end = time.time()
    print('执行时间: %f 秒' % (end-start))
