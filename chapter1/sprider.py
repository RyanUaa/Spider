import urllib.request

response = urllib.request.urlopen('https://www.python3.vip')
print(response.read()).decode('utf-8')