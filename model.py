#coding:utf-8
import sys
from pathlib import Path
import json
import sqlite3

# パスワードの暗号化はあとまわし
# import hashlib

from flask import Flask
app = Flask(__name__)

# データベースファイルのパス
tweet_db_path = './sql/tweetData.db'
user_db_path = './sql/userInfo.db'

# tweetData(sqlite3) => id, tweet_path
# データベースへの接続、使用準備


def registration_user(id, name, email, password):
    '''
    入力された情報をもとに。ユーザ情報をデータベースに格納する。
    それと同時にtweetを格納するJSONを作成する
    今回はパスワードは暗号化していない。
    '''

    sql =   '''
            INSERT INTO users (user_id, user_name, user_email, password)
            VALUES (?, ?, ?, ?)
            '''
    data_execute(sql, (id, name, email, password))

    user_data_path = '/data/' + str(id) + '.json'
    with open(user_data_path,'w') as f:
        free_dict = {}
        json_data = json.dump(free_dict, f, indent=4)
        sql2 =  '''
                INSERT INTO tweetData (id, tweetPath)
                VALUES (?, ?)
                '''
        tweet_execute(sql, (id, user_data_path))



def update_user_id(session, new_id):
    '''
    現在のセッション情報をもとに、user_idを変更する
    '''

    sql =   '''
            UPDATE users
            SET user_id = ? 
            WHERE user_id = ?
            '''
    old_id = session['user_id']

    
    data_execute(sql, (old_id, new_id))#変更だからT or F

def update_user_data(session, key, data):
    '''
    現在のsession情報を元に、ユーザの登録情報を変更する
    '''
    user_id = session['user_id']
    sql =  f'''
            UPDATE users
            SET {key} = {data}
            WHERE user_id = {user_id}
            '''
    try:
        tweet_execute(sql)
        return True
    except:
        #todo ここではエラーを握りつぶしているけど、本当はエラーログを取得ぐらいはしたい            
        return False


def get_tweet(session):
    '''
    その本人のtweetデータのパスをsqlから取得する
    てかツイートデータはユーザごとに一つのJSONファイルに格納する方がよくね
    だから取得するのは、ユーザツイートデータの入ったJSON自体
    '''
    user_id = session['user_id']

    sql =  f'''
            SELECT tweet_path
            FROM tweetData
            WHERE user_id = {user_id}
            '''
    #todo 型は合わせるべきだよなあ、うまくいくと、list返されるだろうし => list???
    try:
        return tweet_execute(sql)
    except:
        return None


def post_tweet(session, tweet_data):
    '''
    tweetされたデータのパスをsqlに格納する
    格納するディレクトリは固定して、ファイル名とかはハッシュを使えばいいかな？
    '''
    user_id = session['user_id']
    sql =  f'''
            INSERT INTO tweetData(user_id, tweet_path)
            VALUES (?, ?)
            '''
    try:
        tweet_execute(sql,(user_id, tweet_data))
        return True
    except:
        return False

def get_tweet_word(path):
    '''
    ファイルパスを受け取り、それからテキストデータを返却する
    '''
    with open (path, "r", encoding="utf-8")as f:
        return f.read()

def store_tweet_word(word):
    '''
    テキストデータ受け取り、ファイルを格納
    ちなみにデータベースにもパスを格納する
    '''
    pass



def tweet_execute(sql, values=None):
    '''
    tweetのデータに関して、sql操作を実行する
    '''
    try:
        connect_tweet_db = sqlite3.connect(tweet_db_path)
        tweet_cursor = connect_tweet_db.cursor()
        tweet_cursor.execute(sql, values)

        tweet_cursor.commit()
        tweet_cursor.close()
    except:
        return False
    

def data_execute(sql, values=None):
    '''
    ユーザデータに関して、sql操作を実行する
    '''
    try:
        connect_user_db = sqlite3.connect(user_db_path)
        user_cursor = connect_user_db.cursor()
        user_cursor.execute(sql, values)

        user_cursor.commit()
        user_cursor.close()
    except:
        return False