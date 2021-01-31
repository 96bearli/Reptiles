#!python
import re
import json
import requests
from time import sleep

def get_data(id):
    baseurl = "http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById"
    data = {'id':id}
    # headers = {"user-agent": "Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36}"
    headers = {"user-agent":"Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36"}
    response_data = requests.post(url = baseurl,data = data,headers=headers).json()
    return response_data


def main():
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    headers = {
            "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36"
            }
    # id_lists = []
    for i in range(366):
        page = i+1
        data = {
                'on': "true",
                'page': page,
                'pageSize':"15",
                'productName': "",
                'conditionType':"1",
                'applyname':"",
                'applysn': ""
                }
        response = requests.post(url = url,data = data,headers=headers).json()
        id_list = re.findall("'ID': '(.+?)'",str(response))
        for id in id_list:
            print(id)
            data = get_data(id)
            print(data['productSn'])
            print(data['epsName'])
            # id_lists.append(id)
        print("page:%s"%page)
        sleep(0.5)


main()
