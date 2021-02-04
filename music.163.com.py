#!python3
import re
import requests
import os
import eyed3

# 搜索关键词，自选下载歌曲
# 想要继续实现的功能
# 音乐详细信息 > 标题 艺术家已实现
# 循环搜索获取歌曲 > 完成
# 下载歌单 > api限制10首
# 随机获取一首热榜歌曲 > over
# 内嵌专辑图片
# 内嵌lrc歌词
headers = {
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36'}


def get_ids(key_word):
    url = "https://v1.alapi.cn/api/music/search?keyword="
    song_url = url + key_word
    response = requests.get(url=song_url, headers=headers).text
    # print(response)
    # data = re.findall(re.compile('"id": (\d+?),\n +?"name": "(.+?)",\n +?"artists"'), response)
    # 这个正则匹配的文本有重复性，所以从两侧开始写正则，中间用特殊的部分分割上下
    find_data = re.compile(
        r'{.+?"id": (\d+?),.+?"name": "(.+?)",.+?"artists".+?\{.+?"id".+?"name": "(.+?)",.+?"album":.+?},', re.S)
    data = re.findall(find_data, response)
    return data


def song_info(alist):
    audiofile = eyed3.load('./cache/' + alist[1] + "_" + alist[2] + '.mp3')  # 读取mp3文件
    audiofile.initTag()  # 初始化所有标签信息，将之前所有的标签清除
    audiofile.tag.artist = alist[2]  # 参与创作的艺术家
    audiofile.tag.album = "None"  # 唱片集
    audiofile.tag.album_artist = "None"  # 唱片艺术家
    audiofile.tag.title = alist[1]  # 标题
    audiofile.tag.track_num = 4  # 音轨编号，专辑内歌曲编号："#"
    audiofile.tag.save()  # 保存文件


def get_song(alist):
    url = "http://music.163.com/song/media/outer/url?id=" + alist[0] + ".mp3"
    print("url:" + url, "\nBegin to download!")
    response = requests.get(url=url, headers=headers).content
    if not os.path.exists("./cache"):
        os.mkdir('d:/music')
    with open('./cache/' + alist[1] + "_" + alist[2] + '.mp3', "wb") as f:
        f.write(response)
    print("Get it!Begin to write Song_info")
    try:
        song_info(alist)
    except Exception as e:
        print("* Song_info failed to change")
        print(e)
    print("Done!Please check ./cache/" + alist[1] + "_" + alist[2] + '.mp3')
    print("-" * 20)


def get_a_song():
    key_word = input("请输入关键词（例如:雪之花）：")
    if key_word == "rand":
        get_random()
        return
    id_name_list = get_ids(key_word)
    print("根据以下列表，您要获取的music为？")
    for id_name in id_name_list:
        print("No." + str(id_name_list.index(id_name)), id_name[1], id_name[2], sep="\t")
    try:
        count = int(input("No."))
    except:
        print("default No.0")
        count = 0
    get_song(id_name_list[count])


def get_playlist(play_id):
    print(play_id)
    url = "https://v1.alapi.cn/api/music/playlist?"
    response = requests.get(url + play_id, headers=headers)
    # requests.request("POST", url, data=play_id, headers=headers)
    find_nickname = re.compile(r'"nickname": "(.+?)",.+?"signature": "(.+?)",', re.S)
    nickname = re.findall(find_nickname, response.text)[0]
    print("歌单作者:" + nickname[0])
    print(nickname[1])
    print("-" * 20)
    find_info = re.compile(r'"name": "(.+?)",.+?"id": (\d+?),.+?"user_name": "(.+?)".+?}', re.S)
    info_list = re.findall(find_info, response.text)
    # print(info_list,len(info_list),sep="\n")
    print("开始依次下载")
    print("-" * 20)
    for info in info_list:
        print("当前进度:%d/%d" % (info_list.index(info) + 1, len(info_list)))
        info_list2 = [info[1], info[0], info[2]]
        get_song(info_list2)
    print("全部下载完毕")


def get_random():
    chose_list = ["热歌榜", "热歌榜", "新歌榜", "飙升榜", "抖音榜", "电音榜"]
    num = input("有什么目标么?比如:\n1.热歌榜\n2.新歌榜\n3.飙升榜\n4.抖音榜\n5.电音榜\n你的选择是:")
    try:
        parm = chose_list[int(num)]
    except:
        print("default \"热歌榜\"")
        parm = chose_list[0]
    url = "https://api.uomg.com/api/rand.music?sort=" + parm + "&format=json"
    response = requests.get(url, headers=headers).text
    # {"code":1,"data":{"name":"丹青墨绿 (Live)","url":"http://music.163.com/song/media/outer/url?id=1812206850","picurl":"http://p4.music.126.net/vHpqZJj-wy6d5QqbgfYfdg==/109951165630898846.jpg","artistsname":"张含韵"}}
    find_info = re.compile(r'"name":"(.+?)","url":".+?id=(\d+?)".+?"artistsname":"(.+?)"', re.S)
    info = re.findall(find_info, response)[0]
    # print(response)
    # print(info)
    info_list2 = [info[1], info[0], info[2]]
    print("Roll到了一首'%s'的'%s'，开始下载咯" % (info[2], info[0]))
    get_song(info_list2)


if __name__ == '__main__':
    print("本工具用于搜索并下载来自网易云音乐的免费播放歌曲\n请选择功能:\n* 1.搜索并获取一首歌曲\n* 2.搜索并获取歌曲(循环)\n* 3.输入歌单url下载所有歌曲")
    print("-" * 20)
    chose = input("你的选择是:")
    print("-" * 20)
    if chose == "1":
        print("搜索获取一首歌曲")
        get_a_song()
    elif chose == "2":
        print("循环搜索获取歌曲")
        i = 0
        while True:
            i += 1
            print("循环运行第%d次" % i)
            if i%3==0:
                print("* 小提示:可以试试关键词输入'rand'")
            get_a_song()
    elif chose == "3":
        id_input = input("Web_api限制，只能获取前10首\n请输入歌单url:")
        try:
            playlist_id = re.findall(r"playlist\?(id=\d+)", id_input)[0]
            # https://music.163.com/#/playlist?id=6589223871
        except:
            try:
                playlist_id = re.findall(r"(id=\d+)", id_input)[0]
            except:
                playlist_id = "id=" + re.findall(r"\d+", id_input)[0]
        get_playlist(playlist_id)
    else:
        print("既然没有选择，那就随机来一首?")
        get_random()
