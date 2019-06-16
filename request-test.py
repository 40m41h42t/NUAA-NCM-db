# coding:utf-8
import requests


def getUserInfo(uid):
    userInfo = requests.get('http://localhost:3000/user/detail?uid=%s' % (uid))
    print(userInfo.json()['profile']['userId'])

getUserInfo('37682214')