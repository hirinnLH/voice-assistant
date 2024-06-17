import json
import math, random
import os

import requests
import vlc
import execjs


def _get_sign(data):
    with open('../utils/qq_music/qq_music_get_sign.js', 'r', encoding='utf-8') as f:
        text = f.read()
    sign = execjs.compile(text).call("getSign", data)
    return sign


def search_all_music(name):
    # headers = {
        # "Cookie": "pgv_pvid=5571744770; pac_uid=0_1f913789b0f97; iip=0; "
        #                  "fqm_pvqid=d17a8a60-8348-4988-b176-0e17265ec116; ts_uid=7973942780; "
        #                  "fqm_sessionid=a4faea25-db60-4a42-9f01-abd1731f942e; pgv_info=ssid=s1026818970; "
        #                  "ts_refer=www.bing.com/; _qpsvr_localtk=0.7326673388556251; "
        #                  "qm_keyst=W_X_63B0aZoLqrHJl16Cpsr3TYjaQtFMAKvVZnTlOTvQwcBZ0fhhxpkN_2zDgJckiO-C0QfD"
        #                  "-tVWGLk2QNkE; euin=oK6kowEAoK4z7eCANeEl7wSPov**; wxuin=1152921504628976741; "
        #                  "wxuin=1152921504628976741; psrf_qqunionid=; "
        #                  "wxrefresh_token=81_J2Wx6aeQgXWFUEIL9-53zgrCjqxgsU99uqNU1-3c"
        #                  "-06LBRlEcRAcb0KZmYEJGoI6H66gffTzyaf8XJ64RU3PsWMTSCBaWcC-UcXHuSx5h_o; psrf_qqaccess_token=; "
        #                  "wxopenid=opCFJw1BuVfi4wFQQJ0jw6MoxxJ8; psrf_qqopenid=; psrf_qqrefresh_token=; "
        #                  "wxunionid=oqFLxsqqE2Mk0g1FvUnLboZ6v5JY; "
        #                  "qqmusic_key=W_X_63B0aZoLqrHJl16Cpsr3TYjaQtFMAKvVZnTlOTvQwcBZ0fhhxpkN_2zDgJckiO-C0QfD"
        #                  "-tVWGLk2QNkE; tmeLoginType=1; "
        #                  "qm_keyst=W_X_63B0aZoLqrHJl16Cpsr3TYjaQtFMAKvVZnTlOTvQwcBZ0fhhxpkN_2zDgJckiO-C0QfD"
        #                  "-tVWGLk2QNkE; login_type=2",
        #        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        #                      "Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"}
    # search type: 0 -> 单曲, 2 -> 专辑, 3 -> 歌单
    qq_music_search_song_body = ('{"comm":{"cv":4747474,"ct":24,"format":"json","inCharset":"utf-8",'
                                 '"outCharset":"utf-8","notice":0,"platform":"yqq.json","needNewCode":1,'
                                 '"uin":"1152921504628976741","g_tk_new_20200303":567410235,"g_tk":567410235},'
                                 '"req_1":{"method":"DoSearchForQQMusicDesktop",'
                                 '"module":"music.search.SearchCgiService","param":{"remoteplace":"txt.yqq.top",'
                                 '"searchid":"71103952445318864","search_type":0,"query":"%s","page_num":1,'
                                 '"num_per_page":10}}}') % name
    sign = _get_sign(qq_music_search_song_body)
    search_url = "https://u6.y.qq.com/cgi-bin/musics.fcg?_=1718614492895&sign=%s" % sign
    json_html = requests.post(search_url, data=qq_music_search_song_body).text  #json格式转化为字典格式 转化的类型必须是字符串型
    search_result = json.loads(json_html)
    return search_result


def give_top_result(search_result: dict, search_type: int):
    top_song_list = []
    if search_type == 0:
        # get all songs info
        music_list = search_result["req_1"]["data"]["body"]["song"]["list"]
    # get top 5 music and give their name
    top_count = 5
    if len(music_list) < 5:
        top_count = len(music_list)
    for i in range(top_count):
        top_song_list[i]["name"] = music_list[i]["name"]  #歌曲名称
        top_song_list[i]["singer"] = music_list[i]["singer"][0]["name"]  #歌手名称
        top_song_list[i]["songmid"] = music_list[i]["songmid"]
    return top_song_list


def get_play_url(search_result: dict, songmid: str):
    # uin = search_result["uin"]
    qq_music_play_url_body = ('{"comm":{"cv":4747474,"ct":24,"format":"json","inCharset":"utf-8","outCharset":"utf-8",'
                              '"notice":0,"platform":"yqq.json","needNewCode":1,"uin":"1152921504628976741",'
                              '"g_tk_new_20200303":11331537,"g_tk":11331537},'
                              '"req_1":{"module":"music.vkey.GetVkey","method":"GetUrl","param":{"guid":"314215786",'
                              '"songmid":["%s"],"songtype":[0],"uin":"1152921504628976741","loginflag":1,'
                              '"platform":"20"}}}') % (songmid)
    sign = _get_sign(qq_music_play_url_body)
    part_play_url = "https://u6.y.qq.com/cgi-bin/musics.fcg?_=1718633534698&sign=%s" % sign
    json_html = requests.post(part_play_url, data=qq_music_play_url_body).text  #json格式转化为字典格式 转化的类型必须是字符串型
    part_play_result = json.loads(json_html)
    purl = part_play_result["req_1"]["data"]["midurlinfo"][0]["purl"]
    play_url = "https://ws6.stream.qqmusic.qq.com/" + purl
    return play_url
#     for music in music_list:
#         per_songmid = music["mid"]  #歌曲的songmid
#         per_songname = music["name"]  #歌曲名称
#         singer = music["singer"][0]["name"]  #歌手名称
#         music_document_url_part = ("https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22req_0%22%3A%7B"
#                                    "%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C"
#                                    "%22param%22%3A%7B%22guid%22%3A%22358840384%22%2C%22songmid%22%3A%5B%22{"
#                                    "}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%221443481947%22%2C%22loginflag"
#                                    "%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A"
#                                    "%2218585073516%22%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D"
#                                    "%7D").format(per_songmid)
#         music_document_html_json = requests.get(music_document_url_part).text
#         music_document_html_dict = json.loads(music_document_html_json)  #将文件从json格式转化为字典格式
#         music_url_part = music_document_html_dict["req_0"]["data"]["midurlinfo"][0]["purl"]  #歌曲下载地址的后部分
#         if music_url_part == "":  #有的没有版权的歌曲应该是没有地址的 所以为空的话 就直接重新循环下一首就行了
#             continue
#         music_url = "https://isure.stream.qqmusic.qq.com/" + music_url_part  #歌曲完整下载地址
#         music_url_content = requests.get(music_url,headers=headers).content  #将歌曲下载地址转化为二进制格式
#         music_file_name = per_songname + "---" + singer + ".mp3"  #歌曲保存的名称  歌曲名+歌手名
#         try:
#             if not os.path.exists(file_address):
#                 os.mkdir(file_address)
#             if not os.path.exists(file_address + music_file_name):
#                 print("正在下载     %s" % music_file_name)
#                 with open(file_address + music_file_name,"wb") as f:  #保存语句
#                     f.write(music_url_content)
#                 print(music_file_name,"   下载成功")
#             else:
#                 print(music_file_name,"   文件已存在")
#         except:
#             print("下载失败")
#
#
# searchAllMusic("风之谷")


all_music = search_all_music("风之谷 久石让")
top_five_result = give_top_result(all_music, 0)
play_url = get_play_url(all_music, top_five_result[1]["songmid"])
# 测试
player = vlc.MediaPlayer(
    play_url)
player.play()
