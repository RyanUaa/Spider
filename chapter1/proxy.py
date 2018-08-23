 #异常处理模块，捕获错误
from urllib.error import URLError        
 #代理IP模块
from urllib.request import ProxyHandler, build_opener   
 
#设置代理IP
proxy_handler = ProxyHandler({
    'http': '127.0.0.0:4973'
})

#通过proxy_handler来构建opener
opener = build_opener(proxy_handler) 
  
#请求网站
try:
    response = opener.open('https://www.baidu.com/')  #此处的open方法同urllib的urlopen方法
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
