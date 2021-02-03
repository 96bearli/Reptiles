#!python3
import re
import requests
import os

headers = {
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36'}


def get_ids(key_word):
    url = "https://v1.alapi.cn/api/music/search?keyword="
    song_url = url + key_word
    response = requests.get(url=song_url, headers=headers).text
    # print(response)
    # data = re.findall(re.compile('"id": (\d+?),\n +?"name": "(.+?)",\n +?"artists"'), response)
    # 这个正则匹配的文本有重复性，所以从两侧开始写正则，中间用特殊的部分分割上下
    find_data = re.compile('{.+?"id": (\d+?),.+?"name": "(.+?)",.+?"artists".+?\{.+?"id".+?"name": "(.+?)",.+?"album":.+?},', re.S)
    data = re.findall(find_data, response)
    # print(len(data))
    # print(data)
    # print(artists)
    # print(len(artists))
    # exit()
    return data


def get_song(alist):
    url = "http://music.163.com/song/media/outer/url?id=" + alist[0] + ".mp3"
    print("下载链接为:" + url, "\n开始下载")
    response = requests.get(url=url, headers=headers).content
    try:
        os.mkdir("./cache")
    except Exception as e:
        print("-"*20)
    with open('./cache/' + alist[1]+"_"+alist[2] + '.mp3', "wb") as f:
        f.write(response)
    print("Done!Please check './cache'")


if __name__ == '__main__':
    key_word = input("本工具用于搜索并下载来自网易云音乐的歌曲\n请输入关键词（例如:雪之花）：")
    id_name_list = get_ids(key_word)
    print("根据以下列表，您要获取的music为？")
    for id_name in id_name_list:
        print("No." + str(id_name_list.index(id_name)), id_name[1], id_name[2], sep="\t")
    count = int(input("No."))
    get_song(id_name_list[count])
