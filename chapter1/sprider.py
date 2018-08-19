# from urllib import request, parse

# url = 'http://httpbin.org/post'
# headers = {
#     'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' ,
#     'Host':'httpbin.org'
# }

# dic = {
#     'name':'Ryan'
# }

# data = bytes(parse.urlencode(dic), encoding='utf-8')
# req = request.Request(url=url,data=data,headers=headers,method='POST')
# response = request.urlopen(req)

# print(response.read().decode('utf-8'))
a = int(3.6)

print(a)
a = input('请输入：')

b = int('3.14',base=10)

print(b)