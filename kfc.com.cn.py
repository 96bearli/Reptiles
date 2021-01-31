#!python
import requests
import re
url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
headers = {'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36'}
local = input("请输入要查询kfc的关键字：")
data = {"cname":"","pid":"","keyword":local,"pageIndex":"1","pageSize":"10"}
response = requests.post(url = url,data = data,headers=headers).json()
print(response)
count = re.findall("{'rowcount': (\d+?)}",str(response))[0]
print("关键词'%s'下共计%s家kfc"%(local,count))
