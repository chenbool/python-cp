import requests
import json
from bs4 import BeautifulSoup
import re
import execjs
import os
maoxian_url = 'http://www.1kkk.com/manhua-list-tag2-p1/'
s = requests.Session()
imgheader ={
#GET http://manhua1032-101-69-161-98.cdndm5.com/1/432/772307/5_1902.jpg?cid=772307&key=a10bca0307a03f6be17ad4ee49ab3e6e&uk= HTTP/1.1
	'Host': 'manhua1032-101-69-161-98.cdndm5.com',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
	'Referer': 'http://www.1kkk.com/ch932-772307/',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.9',
}

s.headers.update(imgheader)
headers = {
	'Host': 'www.1kkk.com',
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'Accept': '*/*',
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	'Referer': 'http://www.1kkk.com/ch932-772307/',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.9',
}

def get_list(url):
	response = requests.get(url,headers=headers)
	cookie = response.cookies
	print(response.status_code)
	soup = BeautifulSoup(response.text,features="lxml")
	div_list = soup.find_all('div',attrs={'class':'mh-item-tip-detali'})
	for div in div_list:
		href = div.h2.a['href']
		name = div.h2.a.text
		get_chapter("http://www.1kkk.com"+href,name,cookie)

# 补全获得章节的代码
def get_chapter(url,name,cookie):
	print(name,url)
	try:
		os.mkdir(name)
	except Exception as e:
		print(e)
	response = requests.get(url,headers=headers,cookies=cookie)
	print(response.status_code)
	cookie = response.cookies
	soup = BeautifulSoup(response.text,features='lxml')
	group = soup.find("div",attrs={'class':'detail-list-title'})
	group_title = []
	a_list = group.find_all("a")
	for a in a_list[:-2]:
		group_title.append(a.text.split("（")[0])
	group_child = []
	group_ul = soup.find_all("ul",attrs={"class":"view-win-list detail-list-select"})
	for ul,title in zip(group_ul,group_title):
		get_group_child(ul,title,name,cookie)

def get_group_child(ul,title,name,cookie):
	lilist = ul.find_all("li")
	for li in lilist:
		# print(li.text)
		charpter_name = li.text.split("（")[0].strip()
		print(li.a['href'])
		download_img_from_url('http://www.1kkk.com'+li.a['href'],li.text.strip().split("（")[-1].split("P")[0],title,name,cookie,charpter_name)



def get_parm(text):
	parm = {}
	DM5_MID = re.findall(r'var DM5_MID=(.*?);',text)
	if len(DM5_MID)>0:
		parm['DM5_MID']=DM5_MID[0]
	else:
		parm['DM5_MID'] = ''
	DM5_VIEWSIGN = re.findall(r'DM5_VIEWSIGN="(.*?)";',text)
	if len(DM5_VIEWSIGN)>0:
		parm['DM5_VIEWSIGN']=DM5_VIEWSIGN[0]
	else:
		parm['DM5_VIEWSIGN'] = ''
	DM5_VIEWSIGN_DT = re.findall(r'DM5_VIEWSIGN_DT="(.*?)";',text)
	if len(DM5_VIEWSIGN_DT)>0:
		parm['DM5_VIEWSIGN_DT']=DM5_VIEWSIGN_DT[0]
	else:
		parm['DM5_VIEWSIGN_DT'] = ''
	print(parm)
	return parm


def download_img_from_url(url,num,title,name,cookie,charpter_name):
	try:
		os.mkdir(name+"/"+title)
	except Exception as e:
		print(e)
	try:
		os.mkdir(name+'/'+title+'/'+charpter_name)
	except Exception as e:
		print(e)
		return
	res = requests.get(url,headers=headers,cookies=cookie)
	cookie = res.cookies
	cid = url.split('-')[-1][:-1]
	print(cid)
	parm = get_parm(res.text)
	page = 1
	while page<=int(num):
		link = "http://www.1kkk.com/ch932-772307/chapterfun.ashx?cid="+cid+"&page="+str(page)+"&key=&language=1&gtk=6&_cid="+cid+"&_mid="+parm['DM5_MID']+"&_dt="+parm['DM5_VIEWSIGN_DT']+"&_sign="+parm['DM5_VIEWSIGN']
		link_response = requests.get(link,headers=headers,cookies=cookie)
		img_result = execjs.eval(link_response.text)
		cookie = link_response.cookies
		for img in img_result:
			img_response = s.get(img,headers=imgheader)
			print(img_response)
			print(img)
			if img_response.status_code!=200:
				exit()
			f = open(name+'/'+title+'/'+charpter_name+'/'+str(page)+'.jpg','wb')
			f.write(img_response.content)
			f.close()
			page = int(img.split("_")[0].split("/")[-1])+1

get_list(maoxian_url)

