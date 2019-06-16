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


class SearchForm(FlaskForm):
    keyword = StringField('关键字', validators=[DataRequired(), Length(1, 40)])
    submit = SubmitField('搜索')


class LocalSearchForm(FlaskForm):
    keyword = StringField('关键字', validators=[DataRequired(), Length(1, 40)])
    select = SelectField(
        '类别',
        choices=[
            ('songName', '歌名'),
            ('authorName', '作者'),
            ('albumName', '专辑')
        ]
    )
    tag = BooleanField('模糊搜索')
    submit = SubmitField('搜索')


class EditUserForm(FlaskForm):
    nickname = StringField('昵称', validators=[DataRequired(), Length(1, 40)])
    signature = StringField('签名', validators=[Length(0, 0x1000)])
    submit = SubmitField('提交修改')
# 以下为路由项


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/user', methods=['GET', 'POST'])
# 用户路由
def user():
    return render_template('user.html', info=db.GetTable('user'))


@app.route('/music', methods=['GET', 'POST'])
# 音乐路由
def music():
    return render_template('music.html', info=db.GetTable('song'))


@app.route('/delete', methods=['GET', 'POST'])
# 删除本地音乐
def delete():
    songId = request.args.get('songId')
    if db.DeleteSongBySongId(songId):
        return "删除成功"
    else:
        return "删除失败"


@app.route('/online_search', methods=['GET', 'POST'])
# 搜索路由
def online_search():
    data = None
    if request.method == 'POST':
        data = ncmapi.OnlineSearch(request.form.get('keyword'))
        # print(data)
    form = SearchForm()
    return render_template('online_search.html', form=form, data=data)


@app.route('/add', methods=['GET', 'POST'])
# 与在线搜索配套的添加
def add():
    songId = request.args.get('songId')
    songData = ncmapi.GetMusicInfoBySongId(songId)
    if db.AddSongDataByDirectory(songData) is True:
        return "添加成功"
    else:
        return "添加失败"


@app.route('/playlists', methods=['GET', 'POST'])
# 用户-歌单路由
def playlists():
    uid = request.args.get('uid')
    return render_template('playlists.html', nickname=db.UserNameFromID(uid), playLists=db.GetPlayList(uid))


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    id = request.args.get('id')
    songLists = db.GetSongList(id)
    return render_template('playlist.html', listName=db.ListNameFromId(id), songs=songLists)


@app.route('/local_search', methods=['GET', 'POST'])
def local_search():
    data = None
    if request.method == 'POST':
        toSearch = {}
        toSearch['keyword'] = request.form.get('keyword')
        toSearch['select'] = request.form.get('select')
        toSearch['tag'] = request.form.get('tag')
        # print(toSearch)
        data = db.SearchLocalSong(toSearch)
    form = LocalSearchForm()
    return render_template('local_search.html', form=form, data=data)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    
    userId = request.args.get('userId')
    if not userId:
        return "空参数"
    if request.method == 'POST':
        newName = request.form.get('nickname')
        newSign = request.form.get('signature')
        if db.EditUserInfo(userId, newName, newSign):
            return "修改成功"
        else:
            return "修改失败"
    userInfo = db.UserInfoFromId(userId)[0]
    form = EditUserForm()
    return render_template('edit.html', form = form, PreData=userInfo)


if __name__ == '__main__':
    app.run(debug=True)
