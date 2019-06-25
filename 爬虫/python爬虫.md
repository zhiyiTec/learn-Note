# 1.引入对应的包
```python
import urllib.request
```
具体如何实现爬虫,比如说爬取一个页面对应的代码，然后在代码中进行过滤：
```
import urllib.request
page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page) #此处设置爬取的网址
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' # 此处设置对付”反盗链”的方式，对付防盗链，服务器会识别headers中的referer是不是它自己，如果不是，有的服务器不会响应，所以我们还可以在headers中加入referer
headers = { 'User-Agent' : user_agent } #此处设置data
# try里面的的就是爬取的核心代码
try:
    request = urllib.request.Request(url,headers = headers)
    response =urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
    items = re.findall(pattern,content)
    for item in items:
        print item[0],item[1],item[2],item[3],item[4]
except urllib.error.URLError as e:
    if hasattr(e,"code"):
        print (e.code)
    if hasattr(e,"reason"):
        print (e.reason)