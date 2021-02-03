#!python
import requests
import json
import re


def translate():
    post_url = "https://fanyi.baidu.com/sug"
    word = input("Input a word:")
    data = {"kw": word}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36"}
    try:
        response = requests.post(url=post_url, data=data, headers=headers)
    except:
        print("未找到释义！")
        exit()
    dic_obj = str(response.json())
    # print(dic_obj)
    # findk = re.compile(r'"k": "(.*?)"')
    findk = re.compile(r"'k': '(.*?)'")
    keys = re.findall(findk, dic_obj)
    # findv = re.compile(r'"v": "(.*?)"')
    findv = re.compile(r"'v': '(.*?)'")
    values = re.findall(findv, dic_obj)
    print("-" * 20)
    if len(keys) == 0:
        print("无释义")
        print('-' * 20)
        exit()
    for i in range(len(keys)):
        print("【" + keys[i] + "】:\t" + values[i])
    print("-" * 20)
    print("结果来自百度翻译")


translate()
