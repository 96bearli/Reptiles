#!python
import re
import requests
url ="https://movie.douban.com/j/chart/top_list"
param = {
        "type":"11",
        "interval_id":"100:90",
        "action":"",
        'start':"0", # 开始于
        "limit":"20" # 多少个
        }
headers = {"user-agent":'Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36'}
list_data = requests.get(url = url,params = param,headers = headers).json()
list_data = str(list_data)
title_list = re.findall("'title': '(.+?)'",str(list_data))
print(title_list)
