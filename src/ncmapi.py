# coding:utf-8
import requests

def OnlineSearchMusic(keyword):
    if not keyword:
        return None
    url = 'http://localhost:3000/search?keywords=%s' % (keyword)
    data = requests.get(url).json()
    ret = []
    for song in data['result']['songs']:
        # print(song)
        d = {}
        d['songId'] = song['id']
        d['songName'] = song['name']
        d['authorId'] = song['artists'][0]['id']
        d['authorName'] = song['artists'][0]['name']
        d['albumId'] = song['album']['id']
        d['albumName'] = song ['album']['name']
        # print(d)
        ret.append(d)
    # print(ret)
    return ret

def GetMusicInfoBySongId(songId):
    url = 'http://localhost:3000/song/detail?ids=%s' % songId
    # print('[+] SongUrl: ', url)
    song = requests.get(url).json()['songs'][0]
    d = {}
    d['songId'] = song['id']
    d['songName'] = song['name']
    d['artistId'] = song['ar'][0]['id']
    d['artistName'] = song['ar'][0]['name']
    d['albumId'] = song['al']['id']
    d['albumName'] = song ['al']['name']
    d['albumPic'] = song['al']['picUrl']
    # print(d)
    return d

def GetUserPlayListByUserId(uid):
    url = 'http://localhost:3000/user/playlist?uid=%s' % uid
    data = requests.get(url).json()['playlist']
    ret = []
    userName = data[0]['creator']['nickname']
    for playlist in data:
        if str(playlist['userId']) != uid:
            break 
        d = {}
        d['userId'] = playlist['userId']
        d['listId'] = playlist['id']
        d['listName'] = playlist['name']
        ret.append(d)
    return userName, ret

def GetSongsListByPlayListId(listId):
    url = 'http://localhost:3000/playlist/detail?id=%s' % listId
    songId = requests.get(url).json()
    listInfo = {}
    listInfo['listName'] = songId['playlist']['name']
    listInfo['listId'] = songId['playlist']['id']
    listInfo['description'] = songId['playlist']['description']
    songsInfo = []
    for songInfo in songId['playlist']['tracks']:
        d = {}
        d['songId'] = songInfo['id']
        d['songName'] = songInfo['name']
        d['artistId'] = songInfo['ar'][0]['id']
        d['artistName'] = songInfo['ar'][0]['name']
        d['albumId'] = songInfo['al']['id']
        d['albumName'] = songInfo['al']['name']
        d['albumPic'] = songInfo['al']['picUrl']
        songsInfo.append(d)
    return listInfo, songsInfo

def OnlineSearchUser(keyword):
    if not keyword:
        return None
    url = 'http://localhost:3000/search?keywords=%s&type=1002' % (keyword)
    data = requests.get(url).json()
    ret = []
    for user in data['result']['userprofiles']:
        d = {}
        d['userId'] = user['userId']
        d['nickname'] = user['nickname']
        d['signature'] = user['signature']
        # print(d)
        ret.append(d)
    print(ret)
    return ret

def OnlineSearchApi(keyword, category):
    if category == 'userName':
        return OnlineSearchUser(keyword)
    elif category == 'songName':
        return OnlineSearchMusic(keyword)


