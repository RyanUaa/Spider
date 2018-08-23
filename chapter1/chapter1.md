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

该函数是本段代码的核心，也是最基本的方法，它通过参数（一个url），可以实现GET请求，获取到网页内容，也就是网页源代码。

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

**Request**

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
  
为什么我们要学习这些请求参数呢，因为一个正确请求，需要正确的参数来构造，才会获得正确的响应，可以说开头就错的话，就步步错了。

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

**Handle**

现在我们已经能够早请求了，但如果我们要设置Cookies或者代理设置等，我们该怎么办呢？

各种Handler来了，利用Handler，我们几乎可以做到所有HTTP请求的所有事情。

首先要知道的是，所有的Handle都是继承来自urllib.request模块的BaseHandler类，它提供了最基本的方法，例如default_open(),protocol_request()等。

一些常见的Handle：

- [ ] **HTTPDefaultErrorHandler**:用于处理HTTP响应错误，错误都会抛出HTTPError类型的异常。
- [ ] **HTTPRedis**:用于处理重定向。
- [ ] **HTTPCookiesProcessor**：用于处理Cookies。
- [ ] **ProxyHandler**：用于设置代理，默认代理为空。
- [ ] **HTTPPasswordMgr**：用于管理密码，它维护了用户名和密码的表。
- [ ] **HTTPBasicAuthHandler**：用于管理认证，如管一个链接打开是需要认证，那么可以用它来解决认证问题。

**Opener**

urllib.urlopen()只能简单的打开一个链接，Request类可以构建了请求对象用于访问，但是在一些HTTP高级处理上：验证、代理、Cookies等，则需要Handler加上Opener来处理。Handler对象通过对应的构造函数产生，Opener则统一用build_opener()方法构造，参数为一个Handler对象，接着用Opener的open()方法就可以打开对应处理之后的链接。这里的open()可以类比urlopen()。

- **验证**
  
    ```python
    from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener
    from urllib.error import URLError

    username = 'example'
    password = 'example' #示例账户、密码
    url = 'https://example.handler/' #示例url

    #构建一个密码管理对象，用来保存需要处理的用户名和密码
    p = HTTPPasswordMgrWithDefaultRealm()

    #添加账户信息，第一个参数realm是与远程服务器相关的域信息，一般没人管它都是写None，后面三个参数分别是 代理服务器、用户名、密码
    p.add_password(None,url,username,password)

    #构建一个代理基础用户名/密码验证的HTTPBasicAuthHandler处理器对象，参数是创建的密码管理对象
    auth_handler = HTTPBasicAuthHandler(p)

    #通过 build_opener()方法使用这些代理Handler对象，创建自定义opener对象，参数包括构建的 proxy_handler 和 proxyauth_handler
    opener = build_opener(auth_handler)

    try:
        result = opener.open(url)
        html = result.read().decode('utf-8')
        print(html)
    except URLError as e:
        print(e.reason)
    ```

    当遇到需要输入账号密码等验证的界面时，我们通过四个步骤来完成：

    1. 构建密码管理对象
    2. 向密码管理对象添加账户信息
    3. 构建HTTPBasicAuthHandler处理器对象
    4. 利用Opner自定义对象访问
   
   当执行完以上步骤时，我们就能看到完成验证之后的界面了，即使验证失败，或者其他原因无法访问，我们也能看到错误的原因。

- **代理**
  
    当我们需要添加代理时：

    ```python   
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
    ```

    返回结果如下：

    ```html
    <html>
        <head>
	        <script>
		        location.replace(location.href.replace("https://","http://"));
	        </script>
        </head>
        <body>
	        <noscript><meta http-equiv="refresh" content="0;url=http://www.baidu.com/"></noscript>
        </body>
    </html>
    ```
    
    Proxyhandler是一个字典，键名为协议类型，键值为代理链接，可以添加多个代理。同样利用这个Handler及build_opener()方法构造的Operner，然后发送请求即可。

- **Cookies**
  
  Cookies同样需要相关Handler,我们先看看内置的http包中的Cookies相关模块：
 
    - CookieJar
        - 管理储存cookie，像传出的http请求添加cookie
        - cookie存储在内存中，CookieJar示例回收后cookie将自动消失
    - FileCookieJar
        - 是CookieJar的字类
        - cookie保存在文件中
    - MozillaCookiejar
        - 是FileCookieJar的子类
        - 与moccilla浏览器兼容
    - LwpCookieJar
        - 是FileCookieJar的子类
        - 与libwww-perl标准兼容

    我们先看看如何将网站的Cookies获取下来：

    ```python
    
    ```
## 处理异常



## 解析链接

## 分析Robots协议