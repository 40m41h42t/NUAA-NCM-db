# coding:utf-8
# 引入 Flask 包
from flask import Flask, render_template, request
# 引入一些 Flask 工具
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
# 引入 Bootstrap
from flask_bootstrap import Bootstrap
# 自己写的数据库操作
import db
# 网易的API
import ncmapi
# 初始化应用程序
app = Flask(__name__)
# secret key 没有必要
app.secret_key = 'alpha'
# 创建Bootstrap模板
bootstrap = Bootstrap(app)


class LocalSearchForm(FlaskForm):
    keyword = StringField('关键字', validators=[DataRequired(), Length(1, 40)])
    select = SelectField(
        '类别',
        choices=[
            ('songName', '歌名'),
            ('artistName', '作者'),
            ('albumName', '专辑'),
            ('listName', '歌单')
        ]
    )
    tag = BooleanField('模糊搜索')
    submit = SubmitField('搜索')


class OnlineSearchForm(FlaskForm):
    keyword = StringField('关键字', validators=[DataRequired(), Length(1, 40)])
    select = SelectField(
        '选项',
        choices=[
            ('songName', '歌名'),
            ('userName', '用户名')
        ]
    )
    submit = SubmitField('搜索')


class EditListForm(FlaskForm):
    listName = StringField('歌单名称', validators=[DataRequired(), Length(1, 40)])
    description = StringField('描述', validators=[Length(0, 0x1000)])
    submit = SubmitField('提交修改')

# 以下为路由项


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


'''
Online
'''


@app.route('/online_search', methods=['GET', 'POST'])
def online_search():
    userData = None
    songData = None
    retdata = None
    form = OnlineSearchForm()
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        category = request.form.get('select')
        print(keyword, category)
    # print(keyword, category)
        if category == 'userName':
            userData = ncmapi.OnlineSearchApi(keyword, category)
        elif category == 'songName':
            songData = ncmapi.OnlineSearchApi(keyword, category)
        return render_template('online_search.html', form=form, userData=userData, songData=songData)
    if request.method == 'GET':
        songId = request.args.get('add')
        print(songId)
        if songId:
            songData = ncmapi.GetMusicInfoBySongId(songId)
            if db.AddSongDataByDirectory(songData) is True:
                retdata = "添加成功"
            else:
                retdata = "添加失败，数据库中已有相关歌曲"
    return render_template('online_search.html', form=form, retdata=retdata)


@app.route('/online_userplaylist', methods=['GET', 'POST'])
def online_userplaylist():
    userId = request.args.get('uid')
    if not userId:
        return "非法参数"
    userName, userPlayList = ncmapi.GetUserPlayListByUserId(userId)
    # print(userPlayList)
    return render_template('online_userplaylist.html', userPlayList=userPlayList, nickname=userName)


@app.route('/online_playlist', methods=['GET', 'POST'])
def online_playlist():
    listId = request.args.get('id')
    if not listId:
        return "非法参数"
    listName, MusicLists = ncmapi.GetSongsListByPlayListId(listId)
    return render_template('online_playlist.html', listId=listId, listName=listName, musicList=MusicLists)


@app.route('/add', methods=['GET', 'POST'])
# 与在线搜索配套的添加
def add():
    songId = request.args.get('songId')
    if songId:
        songData = ncmapi.GetMusicInfoBySongId(songId)
        if db.AddSongDataByDirectory(songData) is True:
            retdata = "添加成功"
        else:
            retdata = "添加失败，数据库中已有相关歌曲"
        return render_template('actionresult.html', data=retdata)
    listId = request.args.get('listId')
    if listId:
        ListInfo, SongsInfo = ncmapi.GetSongsListByPlayListId(listId)
        if SongsInfo:
            db.AddSongsListsTracks(SongsInfo, ListInfo)
            retdata = "添加成功"
        else:
            retdata = "添加失败"
        return render_template('actionresult.html', data=retdata)


'''
Local
'''


@app.route('/local_search', methods=['GET', 'POST'])
def local_search():
    form = LocalSearchForm()
    form.tag.data = 'y'
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        choice = request.form.get('select')
        tag = request.form.get('tag')
        SearchData = db.SearchLocalInfo(keyword, choice, tag)
        return render_template('local_search.html', form=form, choice=choice, Data=SearchData)
    return render_template('local_search.html', form=form)


@app.route('/local_playlists', methods=['GET', 'POST'])
def local_playlists():
    return render_template('local_playlists.html', PlayListsData=db.GetTable('playlist'))


@app.route('/local_playlist', methods=['GET', 'POST'])
def local_playlist():
    listId = request.args.get('id')
    if not listId:
        return "非法参数"
    ListData = db.GetPlayList(listId)[0]
    SongData = db.GetSongList(listId)
    return render_template('local_playlist.html', listData=ListData, songData=SongData)


@app.route('/local_music', methods=['GET', 'POST'])
def local_music():
    return render_template('local_music.html', data=db.GetTable('song'))


@app.route('/delete', methods=['GET', 'POST'])
# 删除本地音乐
def delete():
    songId = request.args.get('songId')
    if songId:
        if db.DeleteSongBySongId(songId):
            retdata = "删除成功"
        else:
            retdata = "删除失败"
    listId = request.args.get('listId')
    if listId:
        if db.DeletePlayListByListId(listId):
            retdata = "删除成功"
        else:
            retdata = "删除失败"
    return render_template('actionresult.html', data=retdata)


@app.route('/edit', methods=['GET', 'POST'])
# 修改本地歌单
def edit():
    info = ""
    listId = request.args.get('listId')
    if listId:
        data = db.GetPlayList(listId)[0]
    else:
        return render_template('actionresult.html', data="参数错误")
    if request.method == 'POST':
        # POST, 修改提交到数据库
        newlistName = request.form.get('listName')
        newDescription = request.form.get('description')
        if not newDescription:
            newDescription = 'None'
        if newlistName == data[1] and newDescription == data[2]:
            info = "没有任何修改哦"
        else:
            db.EditPlayListInfo(newlistName, newDescription, data)
            info = "修改成功！"
            data = db.GetPlayList(listId)[0]
    form = EditListForm()
    form.listName.data = data[1]
    form.description.data = data[2]
    return render_template('edit.html',info = info, form=form)

@app.route('/song', methods=['GET', 'POST'])
def LocalSongInfo():
    songId = request.args.get('id')
    if songId:
        songData = db.GetSong(songId)[0]
    else:
        return render_template('actionresult.html', data="参数错误")
    SongListInfo = db.GetSongListInfo(songId)
    return render_template('song.html', songData=songData, Lists = SongListInfo)

if __name__ == '__main__':
    app.run(debug=True)
