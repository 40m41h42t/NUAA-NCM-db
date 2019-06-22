# coding:utf-8
import pymysql
import SensitiveInfo

db = pymysql.connect(host='127.0.0.1', user='root',
                     password=SensitiveInfo.password, db='local', charset='utf8')
cur = db.cursor()


def GetTable(tbname):
    sql = "SELECT * FROM `%s`" % (tbname)
    try:
        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
    except Exception as e:
        print(e)
    return data


def UserNameFromID(uid):
    sql = "SELECT nickname FROM user WHERE userId='%s'" % (uid)
    try:
        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
    except Exception as e:
        print(e)
    return data


def UserInfoFromId(uid):
    sql = "SELECT * FROM user WHERE userId='%s'" % (uid)
    try:
        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
    except Exception as e:
        print(e)
    return data


def ListNameFromId(id):
    sql = "SELECT listName FROM playlist WHERE listId='%s'" % id
    try:
        cur.execute(sql)
        data = cur.fetchall()
        # print(data)
    except Exception as e:
        print(e)
    return data


def GetPlayList(listId):
    sql = "SELECT * FROM playlist WHERE listId = '%s'" % (listId)
    try:
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        print(e)
    return data


def GetSong(songId):
    sql = "SELECT * FROM song WHERE songId = '%s'" % (songId)
    try:
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        print(e)
    return data


def GetSongList(id):
    sql = "SELECT * FROM track WHERE listId='%s'" % (id)
    try:
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        print(e)
    ret = []
    if data:
        for track in data:
            songInfo = GetSong(track[0])
            ret.append(songInfo[0])
    return ret

def GetSongListInfo(songId):
    sql = '''
    SELECT * FROM
        (SELECT track.songId, track.listId FROM track
        LEFT JOIN song
        ON track.songId = song.songId) as Search
    WHERE songId = '%s'
    ''' % songId
    try:
        cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        print(e)
        return None
    ListsInfo = []
    for SongList in data:
        ListsInfo.append(GetPlayList(SongList[1])[0])
    return ListsInfo


def AddSongDataByDirectory(songDic):
    sql = "INSERT INTO song(`songId`,`songName`,`artistId`,`artistName`,`albumId`,`albumName`,`albumPic`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        songDic['songId'], pymysql.escape_string(songDic['songName']), songDic['artistId'], pymysql.escape_string(songDic['artistName']), songDic['albumId'], pymysql.escape_string(songDic['albumName']), songDic['albumPic'])
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False


def AddSongsByPlayList(listDic):
    for songDic in listDic:
        AddSongDataByDirectory(songDic)


def DeleteSongBySongId(songId):
    sql = "DELETE FROM song WHERE songId='%s'" % (songId)
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False

def DeletePlayListByListId(listId):
    sql = "DELETE FROM playlist WHERE listId = '%s'" % (listId)
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False

def SearchLocalSong(searchData):
    selectTag = searchData['select']
    fuzzy = False
    keyword = searchData['keyword']
    sql = "SELECT * FROM song WHERE "
    if searchData['tag'] == 'y':
        fuzzy = True
    sql += selectTag + ' '
    if fuzzy is False:
        sql += "= '%s'" % (keyword)
    else:
        sql += "LIKE '%%%s%%'" % keyword
    # print(sql)
    try:
        cur.execute(sql)
        data = cur.fetchall()
        return data
    except Exception as e:
        print(e)
        return None


def EditUserInfo(uid, nickname, signature):
    userData = UserInfoFromId(uid)[0]
    # print(userData)
    sql = "UPDATE user SET "
    if userData[1] == nickname:
        sql += "signature='%s' " % signature
        # EditUserSignature(uid, signature)
    elif userData[2] == signature:
        sql += "nickname='%s' " % nickname
        # EditUserNickname(uid, nickname)
    else:
        sql += "nickname='%s', signature='%s' " % (nickname, signature)
    sql += "WHERE userId = '%s'" % uid
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False

def EditPlayListInfo(newlistName, newdesc, OldData):
    sql = "UPDATE playlist SET "
    if newlistName == OldData[1]:
        sql += "description = '%s' " % db.escape_string(newdesc)
    elif newdesc == OldData[2]:
        sql += "listName = '%s' " % db.escape_string(newlistName)
    else:
        sql += "listName = '%s', description='%s' " % (newlistName, newdesc)
    sql +="WHERE listId = '%s'" % OldData[0]
    print(sql)
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False

def AddPlayListByListInfo(ListInfo):
    desc = ListInfo['description']
    if desc:
        desc = pymysql.escape_string(desc)
    sql = "INSERT INTO playlist(`listId`,`listName`,`description`) VALUES ('%s','%s','%s')" % (
        ListInfo['listId'], pymysql.escape_string(ListInfo['listName']), desc)
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False


def AddTrackBySingleSongAndList(SongId, ListId):
    sql = "INSERT INTO track(`songId`,`listId`) VALUES ('%s','%s')" % (
        SongId, ListId)
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False


def AddTrackBySongsAndList(SongsInfo, ListInfo):
    for Song in SongsInfo:
        AddTrackBySingleSongAndList(Song['songId'], ListInfo['listId'])


def AddSongsListsTracks(SongsInfo, ListInfo):
    AddSongsByPlayList(SongsInfo)
    AddPlayListByListInfo(ListInfo)
    AddTrackBySongsAndList(SongsInfo, ListInfo)


def SearchLocalInfo(keyword, choice, tag):
    sql = 'SELECT * FROM '
    if choice == 'listName':
        sql += "playlist "
    else:
        sql += "song "
    sql += "WHERE "+choice+' '
    if tag == 'y':
        sql += "LIKE '%%%s%%'" % keyword
    else:
        sql += "= '%s'" % (keyword)
    print(sql)
    try:
        cur.execute(sql)
        SearchData = cur.fetchall()
        return SearchData
    except Exception as e:
        print(e)
        return None

