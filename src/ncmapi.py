# coding:utf-8
import requests

def OnlineSearch(keyword):
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
    d['authorId'] = song['ar'][0]['id']
    d['authorName'] = song['ar'][0]['name']
    d['albumId'] = song['al']['id']
    d['albumName'] = song ['al']['name']
    # print(d)
    return d

# GetMusicInfoBySongId('131836')