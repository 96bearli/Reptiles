#!python3
import re
import requests
import os
import eyed3

# 搜索关键词，自选下载歌曲
# 想要继续实现的功能
# 音乐详细信息 > 标题 艺术家已实现
# 循环搜索获取歌曲 > 完成
# 下载歌单 > api限制20首
# 随机获取一首热榜歌曲 > over
# 内嵌专辑图片
# 内嵌lrc歌词
headers = {
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36'}
path = "./cache/"
if not os.path.exists(path):
    os.mkdir(path)


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
    audiofile = eyed3.load(path + alist[1] + "_" + alist[2] + '.mp3')  # 读取mp3文件
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
    path_song = path + alist[1] + "_" + alist[2] + ".mp3"
    with open(path_song, "wb") as f:
        f.write(response)
    print("Get it!Begin to write Song_info")
    try:
        song_info(alist)
    except Exception as e:
        print("* Song_info failed to change")
        print(e)
        os.remove(path_song)
        print("这首音乐很可能没有版权或是会员音乐，已自动删除无效文件")
        print("可自行查看该音乐页面: https://music.163.com/song?id=%s" % alist[0])
        print("-" * 20)
        return
    print("Done!Please check " + path_song)
    print("-" * 20)
    return True


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
    # api_1 limit = 10
    # url = "https://v1.alapi.cn/api/music/playlist?"
    # api_2 limit = 20
    url = "https://music.163.com/api/playlist/detail?"
    heads = {
        "cookie": "_iuqxldmzr_=32; _ntes_nnid=863e13c78a4a5ba7d47e9073faffb647,1605611347172; _ntes_nuid=863e13c78a4a5ba7d47e9073faffb647; NMTID=00OtgIakEtHkOFd80-LpEJ4cXGtlp8AAAF11eUvdQ; WM_TID=NfxKZ2IebwRAEBQEFUd7IuJm%2BGPP%2F%2BX8; __remember_me=true; WEVNSM=1.0.0; WNMCID=mogxjy.1612540448188.01.0; WM_NI=qfu4KxqnJ97WaGzVTs4%2BXWMz%2FbKedmxbshEMMqHDvPIU8mroWYGDEuZZna4S7Hqfv1NMG1OtzRqwQuIQA1YxcQlh90PXCZc68jUzxe6AZyx2Alr7F7Lu7k6AzcSLEQ8Bc3U%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed5c754929aa39bb6598feb8fa3d85a928f8aaab56af1e8add8db679199f8dae72af0fea7c3b92ab3babbd5ca74b3b286dab65da399b6b7d779f8f598b8d072edbe8586e767bcbebd89c8478faf88a5f55c8b8bf88ef165958789a5c87f9a86a282b759f598bf87f53b8e9389d2ce80ba8ebf98d47f8b8f8fd2dc74a18fa489bc3c94888dbbe23efcb69b9bfb6ff69f969afb3a83b4bed8c53d90abf98cb54bbabd9dadc85bfc9eadd4d837e2a3; __csrf=fae4abfee1fd5074e6d23c4941de0766; MUSIC_U=01ffdb13bd0564fc595a65a39457155c74c56d7f5e872149b8efb2f0d2ed18ea0931c3a9fbfe3df2; hb_MA-B407-E266474A0BB8_source=www.163yun.com; JSESSIONID-WYYY=NRn8XlyQ4HUhFUU3WjvsAg%2BR4IrDVN1HcixPbKsjob3XDDb27R74kRnEE1Ta4Z3EOiDAO02fqmp%2BfxNa9hC%2FJxF9Xil3%5C0HhcdhXAbFjTWHqHuFG43seEocXc2TGuGr0EwN%2F8J1Q3UQZ1N8C9%2FmM3GY%5Cn6ZBcWbR5ZkVAV%2F5SzddMVaM%3A1612550671071",
        "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36"
    }
    response = requests.get(url + play_id, headers=heads)
    # find_nickname = re.compile(r'"nickname": "(.+?)",.+?"signature": "(.+?)",', re.S)
    find_nickname = re.compile(r'"nickname":"(.+?)","signature":"(.+?)"')
    # requests.request("POST", url, data=play_id, headers=headers)
    # api_1.re
    # find_info = re.compile(r'"name": "(.+?)",.+?"id": (\d+?),.+?"user_name": "(.+?)".+?}', re.S)
    # api_2.re
    # find_info = re.compile(r'},{"name":"(.+?)","id":(\d+?),.+?"artists":[{"name":"(.+?)","id"', re.S)
    # 这个规则总是莫名其妙多出一节,没办法，学习给截取长度加限制来搞定的
    find_info = re.compile(
        r'\{"name":"(.{1,50}?)","id":(\d*?),"position":\d*?,"alias":\[\],"status":\d*?,"fee":\d*?,"copyrightId":\d*?,"disc":".*?","no":\d*?,"artists":\[\{"name":"(.+?)"',
        re.S)
    nickname = re.findall(find_nickname, response.text)[0]
    print("歌单作者:" + nickname[0])
    print("作者签名:\n" + nickname[1].replace("\\n", "\n"))
    print("-" * 20)
    info_list = re.findall(find_info, response.text)
    with open("./cache/log.txt", "w", encoding="utf-8")as f:
        # f.write(response.text)
        for infos in info_list:
            for info in infos:
                f.write(info + "\n")
            f.write("\n")
    print(len(info_list))
    # return
    print("开始依次下载")
    print("-" * 20)
    success_count = 0
    for info in info_list:
        print("当前进度:%d/%d" % (info_list.index(info) + 1, len(info_list)))
        info_list2 = [info[1], info[0], info[2]]
        if get_song(info_list2):
            success_count += 1
    print("全部下载完毕,成功%i首,失败%i首\n支持正版是音乐创作的动力源泉" % (success_count, len(info_list) - success_count))


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
            if i % 3 == 0:
                print("* 小提示:可以试试关键词输入'rand'")
            get_a_song()
    elif chose == "3":
        id_input = input("Web_api限制，只能获取最多前20首\n请输入歌单url:")
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
        print("既然没有选择，那就随机来几首?")
        try:
            nums = int(input("那么几首呢？说个数："))
        except:
            print("默认一首")
            nums = 1
        for i in range(nums):
            get_random()
            print("第%d次啦" % (i + 1))
        print("结束啦")
    print("-" * 20)
    input("按回车退出程序...")
