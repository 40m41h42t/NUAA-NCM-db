# coding:utf-8
import requests

testUid = '37682214'
# 首先获取用户的相关信息

def getUserInfo(uid):
    url = 'http://localhost:3000/user/detail?uid=%s' % uid
    print("[+] userUrl: ", url)
    data = requests.get(url)
    return data.json()

userJson = getUserInfo(testUid)
print("[+] userId: ",userJson['profile']['userId'])
print("[+] nickname: ", userJson['profile']['nickname'])
print("[+] signature: ", userJson['profile']['signature'])

# 接下来获取用户的歌单信息

def getPlaylists(uid):
    url = 'http://localhost:3000/user/playlist?uid=%s' % uid
    print('[+] UserPlayListUrl: ', url)
    return requests.get(url).json()

playListsJson = getPlaylists(testUid)
i = 0
for playList in playListsJson['playlist']:
    print('[+] Playlist ', i)
    print("    [+] userId: ", playList['userId'])
    print('    [+] listId: ', playList['id'])
    print('    [+] name: ', playList['name'])
    i+=1

# 然后获取一个歌单内所有音乐的信息

testPlaylist = '30315000'
# 其实只需要trackId

def getSongId(listId):
    url = 'http://localhost:3000/playlist/detail?id=%s' % listId
    print('[+] PlayListUrlDetail: ', url)
    return requests.get(url).json()

SongIds = getSongId(testPlaylist)
for id in SongIds['playlist']['trackIds']:
    print('    [+] Song ID: ', id['id'])

# 接下来测试获取音乐信息

testSongId = '445666155'
def getSongInfo(songId):
    url = 'http://localhost:3000/song/detail?ids=%s' % songId
    print('[+] SongUrl: ', url)
    return requests.get(url).json()

SongInfos = getSongInfo(testSongId)
for SongInfo in SongInfos['songs']:
    # print(SongInfo)
    print('[+] songId: ', SongInfo['id'])
    print('[+] songName: ', SongInfo['name'])
    print('[+] author: ')
    for author in SongInfo['ar']:
        print('[+] authorId: ', author['id'])
        print('[+] authorName: ', author['name'])
    print('[+] albumId: ', SongInfo['al']['id'])
    print('[+] albumName: ', SongInfo['al']['name'])