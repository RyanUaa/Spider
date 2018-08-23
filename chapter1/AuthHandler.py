#改代码仅做示例，username、password、url均为示例

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

