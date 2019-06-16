# coding:utf-8
import pymysql
import SensitiveInfo

db = pymysql.connect(host='127.0.0.1', user='root',
                     password=SensitiveInfo.password, db='music', charset='utf8')
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


def GetPlayList(uid):
    sql = "SELECT * FROM playlist WHERE userId = '%s'" % (uid)
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


def AddSongDataByDirectory(songDic):
    sql = "INSERT INTO song(`songId`,`songName`,`authorId`,`authorName`,`albumId`,`albumName`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
        songDic['songId'], songDic['songName'], songDic['authorId'], songDic['authorName'], songDic['albumId'], songDic['albumName'])
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False

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

def SearchLocalSong(searchData):
    selectTag = searchData['select']
    fuzzy = False
    keyword = searchData['keyword']
    if searchData['tag'] == 'y':
        fuzzy = True
    if selectTag == 'songName':
        sql = "SELECT * FROM song WHERE songName "
    elif selectTag == 'authorName':
        sql = "SELECT * FROM song WHERE authorName "
    elif selectTag == 'albumName':
        sql = "SELECT * FROM song WHERE albumName "
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

