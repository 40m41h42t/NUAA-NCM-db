# coding:utf-8
import requests
import pymysql
import SensitiveInfo

testUid = '312517708'
testPlaylist = '30315000'
testssssSongId = '445666155'
# 首先获取用户的相关信息
db = pymysql.connect(host='127.0.0.1', user='root',
                     password=SensitiveInfo.password, db='music', charset='utf8')
cur = db.cursor()


def getUserInfo(uid):
    url = 'http://localhost:3000/user/detail?uid=%s' % uid
    print("[+] userUrl: ", url)
    data = requests.get(url)
    return data.json()


def getPlaylists(uid):
    url = 'http://localhost:3000/user/playlist?uid=%s' % uid
    print('[+] UserPlayListUrl: ', url)
    return requests.get(url).json()


def getSongId(listId):
    url = 'http://localhost:3000/playlist/detail?id=%s' % listId
    print('[+] PlayListUrlDetail: ', url)
    return requests.get(url).json()


def getSongInfo(songId):
    url = 'http://localhost:3000/song/detail?ids=%s' % songId
    print('[+] SongUrl: ', url)
    return requests.get(url).json()


def InsertDbUser():
    userJson = getUserInfo(testUid)
    userId = userJson['profile']['userId']
    nickname = userJson['profile']['nickname']
    signature = userJson['profile']['signature']
    print("[+] userId: ", userId)
    print("[+] nickname: ", nickname)
    print("[+] signature: ", signature)

    sql = "INSERT INTO user(`userId`,`nickname`,`signature`) VALUES ('%s','%s','%s')" % (
        userId, pymysql.escape_string(nickname), pymysql.escape_string(signature))
    print("[+] sql: ", sql)
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        # exit(1)


def InsertIntoPlayList(userId, listId, listName):
    sql = "INSERT INTO playlist(`listId`, `userId`, `listName`) VALUES ('%s','%s','%s')" % (
        listId, userId, pymysql.escape_string(listName))
    print("[+] sql: ", sql)
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        # exit(1)


def InsertDbPlayList():
    # 接下来获取用户的歌单信息
    playListsJson = getPlaylists(testUid)
    i = 0
    for playList in playListsJson['playlist']:
        print('[+] Playlist ', i)
        userId = playList['userId']
        listId = playList['id']
        listName = playList['name']
        print("    [+] userId: ", userId)
        print('    [+] listId: ', listId)
        print('    [+] name: ', listName)
        if str(userId) != testUid:
            break
        InsertIntoPlayList(userId, listId, listName)
        InputSingleList(listId)
        i += 1
# 然后获取一个歌单内所有音乐的信息
# 其实只需要trackId
# 接下来应该首先插入所有音乐,再建立对应的表.


def InsertIntoSong(songId, songName, authorId, authorName, albumId, albumName):
    sql = "INSERT INTO song(`songId`,`songName`,`authorId`,`authorName`,`albumId`,`albumName`) VALUES ('%s','%s','%s','%s','%s','%s')" % (
        songId, pymysql.escape_string(songName), authorId, pymysql.escape_string(authorName), albumId, pymysql.escape_string(albumName))
    print("[+] sql: ", sql)
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        # exit(1)


def InsertDbMusic(testsongId):
    # 接下来测试获取音乐信息
    SongInfos = getSongInfo(testsongId)
    for SongInfo in SongInfos['songs']:
        # print(SongInfo)
        authorId = ''
        authorName = ''
        songId = SongInfo['id']
        songName = SongInfo['name']
        authorId = SongInfo['ar'][0]['id']
        authorName = SongInfo['ar'][0]['name']
        albumId = SongInfo['al']['id']
        albumName = SongInfo['al']['name']
        print('[+] songId: ', songId)
        print('[+] songName: ', songName)
        print('[+] authorId: ', authorId)
        print('[+] authorName: ', authorName)
        print('[+] albumId: ', albumId)
        print('[+] albumName: ', albumName)
        InsertIntoSong(songId, songName, authorId,
                       authorName, albumId, albumName)


def InsertIntoCmpList(listId, songId):
    sql = "INSERT INTO track(`songId`,`listId`) VALUES ('%s','%s')" % (
        songId, listId)
    print("[+] trackSQL: ", sql)
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


def InputSingleList(listId):
    SongIds = getSongId(listId)
    for id in SongIds['playlist']['trackIds']:
        songId = id['id']
        print('    [+] Song ID: ', songId)
        InsertDbMusic(songId)
        InsertIntoCmpList(listId, songId)




def InsertMusicByListId(ListId):
    # 通过歌单导入音乐(只导入音乐)
    SongIds = getSongId(ListId)
    for id in SongIds['playlist']['trackIds']:
        songId = id['id']
        print('    [+] Song ID: ', songId)
        InsertDbMusic(songId)



def InsertListByUid(uid):
# 通过用户导入歌单(只导入歌单)
    playListsJson = getPlaylists(uid)
    i = 0
    for playList in playListsJson['playlist']:
        print('[+] Playlist ', i)
        userId = playList['userId']
        listId = playList['id']
        listName = playList['name']
        print("    [+] userId: ", userId)
        print('    [+] listId: ', listId)
        print('    [+] name: ', listName)
        if str(userId) != uid:
            break
        InsertIntoPlayList(userId, listId, listName)
        # InputSingleList(listId)
        i += 1

# 通过用户歌单建立歌单表与音乐的对应关系
def InsertTrackByListId(listId):
    SongIds = getSongId(listId)
    for id in SongIds['playlist']['trackIds']:
        songId = id['id']
        print('    [+] Song ID: ', songId)
        InsertIntoCmpList(listId, songId)
# InsertDbUser()
# InsertDbPlayList()


# 添加于老板的歌单:
# InsertListByUid('132438426')
# InsertMusicByListId('2587440340')
InsertTrackByListId('2587440340')

cur.close()
db.close()
