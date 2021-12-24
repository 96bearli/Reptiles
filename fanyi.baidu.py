#!python
import requests

def translate():
    post_url = "https://fanyi.baidu.com/sug"
    word = input("Input a word:")
    data = {"kw": word}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36"}
    try:
        response = s.post(url=post_url, data=data, headers=headers)
    except:
        print("未找到释义！")
        return
    obj = response.json()['data']
    print("-" * 20)
    if len(obj) == 0:
        print("无释义")
        print('-' * 20)
        return
    for kv in obj:
        print("【" + kv['k'] + "】:\t" + kv['v'])
    print("-" * 20)
    print("结果来自百度翻译")


if __name__ == '__main__':
    i = 0
    s = requests.session()
    while True:
        i += 1
        print("当前为第%d次查询" % i)
        translate()
