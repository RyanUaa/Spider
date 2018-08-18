# urllib库

---

这是一个HTTP请求库，是Python内置的，在Python2中，有urllib以及urllib2两个库来实现请求的发送，Python3中，整合了两个库，统一为urllib。

该库有四个模块：
|名称|说明|
|:--:|-|
|request|请求模块|
|response| 响应模块|
|error |错误处理模块|
|parse |URL处理模块|
|robotparse |处理机器人协议|

1. urlopen()

## 发送请求

现在写一个最简单的爬虫，实现第一个小功能，爬取网页源代码。要获取源代码，那我们首先应该是发起请求，记住，不管需要服务器为你做什么，都需要先发起请求。

```python
import urllib.request

#调用urllib库中的request模块的urlopen方法,获取一个HTTPresponse对象
response = urllib.request.urlopen('https://www.python.org')

#把该HTTPresponse对象调用read方法读出网页内容，按照utf-8的格式解码之后打印
print(response.read().decode('utf-8'))
```

> urllib.request.urlopen(url,data=None,[timeout,]*,cafile=None,capth=None,cadefault=false,context=None) 

该函数是本段代码的核心，也是最基本的方法，它通过参数（一个url），可以实现GET请求，获取到网页内容。

如果我们的请求是有参数的的，例如POST请求，该怎么做呢。这里就可以用到url的第二个参数data。

**data参数**

这是一个可选参数，当使用到这个参数时，需要传递字节流编码格式的内容，可以使用bytes()方法转换。

```python
import urllib.request
import urllib.parse

data = bytes(urllib.parse.urlencode({'Hello':'World'}), ecnoding='utf-8')

#调用urllib库中的request模块的urlopen方法,获取一个HTTPresponse对象
response = urllib.request.urlopen('https://httpbin.org/post',data)

#把该HTTPresponse对象调用read方法读出网页内容，按照utf-8的格式解码之后打印
print(response.read().decode('utf-8'))
```

> 我们用httpbin.org来测试post请求，他可以输出我们的请求信息。

以下是结果：
```JavaScript
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "Hello": "World"
  },
  "headers": {
    "Accept-Encoding": "identity",
    "Connection": "close",
    "Content-Length": "11",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "httpbin.org",
    "User-Agent": "Python-urllib/3.7"
  },
  "json": null,
  "origin": "180.171.113.184",
  "url": "https://httpbin.org/post"
}
```

我们可以看到，在form字段中，我们传递的字典{'Hello':'World'}参数出现了。

**timeout**

timeout参数用于设置超时时间，单位为秒，如果超出这个时间还没得到响应的话，就会抛出异常。如果不指定该蚕食，则使用全局的默认时间。

```python
import urllib.request

#设置超时时间0.1s
response = urllib.request.urlopen('http://www.google.com',timeout=1)
print(response.read())
```

因为我们设置了0.1秒的超时时间，所以在程序0.1秒后，服务器依然没有响应，会抛出异常：
```
发生异常: URLError
URLError(timeout('_ssl.c:1029: The handshake operation timed out'))
```

可以看出，错误原因就是超时。

所以我们的爬虫，应该在服务器响应超时时，跳过爬取，或是执行其他手段，利用python的try except语句来实现：

```python
import socket
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')
```
运行结果：
```
TIME OUT
```
> 在我们请求服务器响应的过程中，虽然被抽象为只有一个发送请求的动作，但其实底层还有各层协议在需要处理消息，比如DNS服务器解析我们的URL，ARM解析我们的MAC地址，TCP/IP的三次握手建立连接，各层加包头、解包头，再加上网络环境的拥塞控制，基本上0.1s是没办法获取到服务器的响应的，当然，现在如此，未来我们拭目以待。

**其他参数**

除了以上提到的两个参数之外，其他的比如必须是ssl.SSLContext类型的context参数，它用来指定SSL设置。cafile用来指定CA证书和它的路径，这个再请求HTTPS链接时用到。cadefault已经弃用，默认为false。

2. Request

urlopen()方法是最基本的请求方法，而一个完整的请求，远不是这几个参数所能满足的，想要加入Headers等信息，我们利用Request类来构造：
```python
import urllib.request

#通过构造Request对象来请求，而不是直接传url
request = urllib.request.Request('http://python.org')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
```

我们依然使用urlopen()方法来构建这个请求，只不过我们这次该方法参数不再是URL，而是一个Request对象。

Request的构造方法：

> class urllib.request.Request(url,data=None,headers={},origin_req_host=None,unerififiable=False,method=None)

各个参数：

- url 请求链接，必传参数，其余都是可选参数
- data 表单数据，必须为bytes（字节流）类型的。如果它是字典，parse模块的urlencode()方法进行编码
- headers 请求头，字典类型。可以直接再请求时通过headers参数构造，也可以通过调用add_headers()方法添加。
  > 添加请求头最常用的方法就是通过修改User-Agent来伪装浏览器，默认的User-Agent时Python-urllib，比如我们可以通过修改它来伪装成火狐浏览器,设置为：
  > Mozilla/5.0 (x11; U; Linux i686) Gecko/20071227 Fire2.0.0.11
- origin_req_host 指的是请求方的host名称或者IP地址
- unverifiable 表示这个请求是否无法验证，默认false。如果没有权限获取的数据，unverifiable为ture
- method 请求方法，GET、POST、PUT等
  
我们来试一试，传入多个参数：
```python
from urllib import request,parse

url = 'http://httpbin.org/post'
headers = {
    'User-Agent':'Mozilla/5.0 (x11; U; Linux i686) Gecko/20071227 Fire2.0.0.11',
    'Host':'httpbin.org'
}
dic = {
    'name':'Ryan'
}
data = bytes(parse.urlencode(dic),encoding='utf-8')
req = request.Request(url=url,data=data,headers=headers,method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
```
运行结果：
```JavaScript
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "nam": "Ryan"
  },
  "headers": {
    "Accept-Encoding": "identity",
    "Content-Length":"11",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "httpbin.org",
    "User-Agent": "Mozilla/5.0 (x11; U; Linux i686) Gecko/20071227 Fire2.0.0.11"
  },
  "json": null,
  "origin": "180.171.113.184",
  "url": "http://httpbin.org/post"
}
```

我们还可以用add_headers()方法来添加heders:
```python
req = request.Request(url=url, data=data, method='POST')
req = add_headers('User-Agent', 'Mozilla/5.0 (x11; U; Linux i686) Gecko/20071227 Fire2.0.0.11')
```
> *add_headers()源码：*
> ```python
>      def add_header(self, key, val):
>        # useful for something like authentication
>        self.headers[key.capitalize()] = val 
> ```


## 处理异常

## 解析链接

## 分析Robots协议