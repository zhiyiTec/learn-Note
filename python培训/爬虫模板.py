# coding : utf-8
# 团队名称：小卓班
# 开发者： 彭翔
# 开发时间： 2019/9/30 11:12

import re
import requests


# resp = requests.get('http://www.baidu.com')
#
# with open('aaa.txt','w+',encoding='utf-8') as f1:
#     f1.write(resp.text)
#
# print('我拿到了网站的内容')


# respimg =  requests.get('http://www.python.org/static/img/python-logo.png')
#
# with open('D:/baidu.png','wb') as f1:
#     f1.write(respimg.content)
#
# print('我已经把图片爬到了')


booktext = requests.get('https://book.douban.com/').text

pattern = re.compile('<li.*?title="(.*?)".*?src="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>', re.S)
results = re.findall(pattern, booktext)

for book in results:
    title,picurl,zuozhe,year = book
    print('----------')
    print('书名',title)
    print('作者',zuozhe)
    print('时间',year)
    with open('D:/test/'+title+'.jpg','wb') as f1:
        f1.write(requests.get(picurl).content)

print("爬取成功")

