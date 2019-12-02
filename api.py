#coding:utf-8
import sys

from flask import Flask, session, request, redirect, url_for, escape, jsonify
import json
from model import (
    registration_user,
    get_tweet
)

#ここは暫定でテキトーに秘密鍵作っているが、別のところに格納する必要があるな

app = Flask(__name__)

app.secret_key = ${{ secrets.SECRET_KEY }}
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策

@app.route('/')
def index():
    if 'user_id' in session:
        return 'logged in as %s <br><a href="/logout">logout</a>'% escape(session['user_id'])
    # return redirect(url_for('login'))

    return '''You are not logged in</br>
    <a href="/login">login</a>
    '''


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_id'] = request.form['user_id']
        return redirect(url_for('index'))
    
    #ここも暫定の返却、フロントエンドに頑張ってもらう
    return '''
        <form method="post">
            <p><input type=text name=user_id>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/ja')
def helloWorld():
    return 'こんにちはせかい'

@app.route('/<user_id>', methods=['GET'])#todo ここのgetいらん気が
def userPage():
    #現在はログインidとの認証を行なう
    response = {'success':False}
    
    if session['user_id'] != user_id:
        return jsonify(response)
    
    # tweet_dataにはツイートデータのパスが入っている
    tweet_data = get_tweet(session)
    # no check
    # ここでツイートデータを取得
    if tweet_data is None:
        return jsonify(response)
    else:
        response['tweet_data'] = tweet_data
        return jsonify(response)

    '''
    tweet_data = {
        1: "",
        2: "",
        3: ""
    }
    これを返却するのもいいよね
    いつかはネストが深くなるが、日付、文章、添付ファイルリストとか取得したい
    あとlikeみたいなものも必要か？
    '''


    session['success'] = True
    return jsonify(tweet_data)

@app.route('/<user_id>', methods=['POST']
def tweeting():
    '''
    つぶやき（テキストデータ）をファイルに格納、保存する
    {
        "tweeting": "OOOOOOO"
    }
    '''
    tweet_res = {'success': False}
    



# 今回はwebページを用意できていないため、GETで直接送信できるようにした
# @app.route('/registration', methods=["POST"])
@app.route('/registration/<user_id>', methods=['POST'])
def registrate():
    """
    ユーザ登録を行う、まだページを用意してはいないけど、とりあえず用意はする
    """
    data = request.args

    try:
        registration_user(user_id, user_name, user_email, password)
        return "ユーザ登録が完了しました"
    except:
        return "ユーザ登録に失敗しました"


if __name__ == '__main__':
    app.run()