# sprider基础
---
> 在学习爬虫之前，我们应该先知道一些常识，我把它分成三部分：
- `什么是爬虫`
- `我们能用爬虫做什么`
- `怎么爬`

要想说清楚是网络爬虫，我们得先了解网络的构造、网页的组成等等一些基础知识。

---
## 1. HTTP
    先了解HTTP的基本原理，HTTP是网络中应用层的一个协议，我们从在浏览器输入URL开始说起。
### URL URI
> - URI 全称为*Uniform Resource Identifier*  即**统一资源标志符**
> - URL 全称为*Uniform Resource Locator*  即**统一资源定位符**

比方说 [https://www.baidu.com](https://www.baidu.com)是百度的链接链接，这既是一个URL。
而[https://www.baidu.com/img/bd_logo1.png](https://www.baidu.com/img/bd_logo1.png)这是一个定位到百度logo那张图片的URI，各位不妨点击试试。
应该记住的是，URL是URI的一个子集。所以所有的URL都是URI，但不是每一个的URI都是URL。可以理解为URL就是每家的门派地址，而URI则是具体找某样东西（比喻不准确）。一般的网页链接，既可以成为URL，也可以成为URI。

### 超文本

我们在浏览器中看到的页面，都是超文本解析而来的，查看网页源代码时，就能看到其都是`HTML`代码，`HyperText Markup Language 超文本标记语言`，能看到一系列的标签，浏览器就是解析这些标签，对文本做出相应的处理，才呈现出网页的样子，而我们后来要写的爬虫，也会识别这些标签。
任意打开一个网页，任意地方点击鼠标右键，点“检查”，或者 按`f12`，打开浏览器的开发工具，这时在`Elements`下就能看到网页源代码。

### HTTP HTTPS

在百度首页[https://www.baiud.com](https://www.baidu.com)中，我们可以看到，URL的开头会有https或者http。或是还有其他的，我们先不管它。
> - HTTP *Hyper Text Transfer Protocl*超文本传输协议
> - HTTPS *Hyper Text Transfer Protocol over Socket Layer* 

从字面意思就能看出，HTTPS就是安全版本的HTTP，是基于SSL加密实现的安全版本，这里我们不讲HTTP和HTTPS原理，我们要知道的现在的app和网站大多都在向HTTPS发展。

### HTTP请求过程

现在我们终于在浏览器中输入了一个URL，敲一下回车之后，精彩的页面就呈现在我们电脑上了。而在这个表象这下，是我们的浏览器向网站的服务器发送了一个请求，服务器解析我们的请求，返回一个对应的响应。我们的浏览器收到这个包括网页源代码等内容的响应，进行解析，按照相应规则呈现出来。
而我们一般称呼我们的浏览器为客户端，请求的服务器为服务器端，这就是经典的CS模型(`Client/Server`)。

### Request
由客户端发出的，请求的呈现页面。
请求可以分为四个部分：请求方法`Request Method`，请求的网址`Request URL`，请求头`Request Headers`，请求体`Request Body`。

**请求方法**

|序号|方法|描述|
|:----:|:----:|---|
|1|GET|请求指定的页面信息，并返回实体主体。|
|2|HEAD|类似于get请求，只不过返回的响应中没有具体的内容，用于获取报头|
|3|POST|向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修改。|
|4|PUT|从客户端向服务器传送的数据取代指定的文档的内容。
|5|DELETE|请求服务器删除指定的页面。|
|6|CONNECT|HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。|
|7|OPTIONS|允许客户端查看服务器的性能。|
|8|TRACE|回显服务器收到的请求，主要用于测试或诊断。|

**请求地址**

也就是请求的网址，URL。

**请求头**

请求报文的头部信息，用来说明服务器要使用的附加信息，比较重要的信息`Accept`,`Cookie`,`Refer`,`User-Agent`等。

> Accept 

请求报文可通过一个“Accept”报文头属性告诉服务端 客户端接受什么类型的响应。 

> Cookie

这是网站为了辨别用户进行会话跟踪而存储再用户本地的数据。她的主要功能是维持当前的访问会话。

说白了，我们在输入用户名和密码成功登陆其某个网站后，服务器就会用会话保存我们的登陆信息，我们在各个网站之间跳来跳去，第二次访问的时候，服务器看到你的cookies，就会说“哦！是刚才那个家伙”。从而不需要你第二次输入登陆信息。 

> Referer 

表示这个请求是从哪个URL过来的，假如你通过百度搜索出一个商家的广告页面，你对这个广告页面感兴趣，鼠标一点发送一个请求报文到商家的网站，这个请求报文的Referer报文头属性值就是https://www.baidu.com

> User-Agent

简称UA，它可以是服务器识别客户端使用的操作系统以及版本、浏览器及版本等信息。爬虫加上这个信息，可以伪装成浏览器😁。 

**请求体**

请求体一般是针对POST的表单数据，GET的参数直接跟在URL后面，请求体为空。
而POST的内容，一般是我们在浏览器页面中输入的信息，比如账号密码等。
在爬虫中，如果要构造POST请求，需要正确使用Content-Type，并了解各种请求库的各个参数设置时使用的是哪种Context-Type，不然可能会导致POST提交后无法正常响应。具体操作，后面讲到。

### Response

响应，在服务器收到客户端的请求后返回的，可以分为三个部分：相应状态码`Response Status Code`,响应头`Response Headers`,响应体`Response Body`。

**响应状态码**

我们应该都经历过页面无法跳转，显示“404 NOT FOUND”的情况，此时，404就是一个相应状态码。
最常见的是200正常响应，404页面未找到，500服务器异常。
具体可以参考:[https://www.cnblogs.com/jian-99/p/9360588.html](https://www.cnblogs.com/jian-99/p/9360588.html)

**响应头**

一些常用的头部信息：

|字段|	说明|
|:----:|:--|
|Allow|服务器支持哪些请求方法（如GET、POST等）|
|Content-Encoding|文档的编码（Encode）方法。|
|Content-Type|表示后面的文档属于什么MIME类型。Servlet默认为text/plain，但通常需要显式地指定为text/html。由于经常要设置Content-Type，因此HttpServletResponse提供了一个专用的方法setContentType。|
|Date|当前的GMT时间。|
|Expires|指定响应的过期时间|
|Last-Modified|文档的最后改动时间。|
|Server|服务器信息。|
|Set-Cookie|设置和页面关联的Cookie。|

**响应体**

写爬虫，要解析的就是响应体，我们请求的内容，都在请求体中返回给我们了。可以说，只要是在合理合法的范围内，我们可以获取我们可以获得网页上的任意资源，网页源代码、JSON数据等，从而进行解析，是不是有一种银行大门敞开的感觉，但这个大门看似敞开，其实暗藏玄机。

## 2. 网页

*各位有没有想过，为什么不同的网站，是不同的样子？*

### 网页组成

说到网页，就不得不说网页三大部分：`HTML,CSS,JavaScript`。如果把一个网站比喻为一个房间，HTML就是制定了房间的布局，CSS制定了家具的摆放、整体的风格，JavaScript则是规定了在里面的生活方式，

### 网页的构造

我们来看一个最简单的html页面：
```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>这是title<title>
    </head>
    <body>
        <h2>Hello World!</h2>
        <p class="test">这是段落</p>
    </body>
</html>
```
只要知道，所有得源代码，都是这样得形式

### HTML DOM树

### 选择器

## 3. 爬虫
### 概述

### JavaScript 渲染页面

## 4. Session 和 Cookies
### 静态页面和动态页面

### 无状态HTTP

## 5. 代理