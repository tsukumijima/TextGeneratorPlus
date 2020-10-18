# -*- coding: utf-8 -*-

"""
指定されたアカウントの過去のツイートを遡って取得し、pasttweets 以下に (アカウント名).txt という名前で保存するファイル
(アカウント名)_lasttweet.dat があればそのファイルに書き込まれているツイート ID までのツイートを取得する
"""

import os
import sys
import time
import math
import dotenv
import twitter
from pprint import pprint

import oauth2
import urllib

# Windows 環境向けの hack
# 参考: https://stackoverflow.com/questions/31469707/changing-the-locale-preferred-encoding-in-python-3-in-windows
if os.name == 'nt':
    import _locale
    _locale._getdefaultlocale_backup = _locale._getdefaultlocale
    _locale._getdefaultlocale = (lambda *args: (_locale._getdefaultlocale_backup()[0], 'UTF-8'))


class PassTweetstoText:

    def __init__(self, screen_name):

        # 取得するユーザーのスクリーンネーム
        self.screen_name = screen_name.replace('@', '')

        # .env を読み込み
        dotenv.load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '/.env')

        # Twitter API の各種キーを取得
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')

        # 各種キーのいずれかが取得できなかったらエラー
        if (access_token == None or
            access_token_secret == None or
            consumer_key == None or
            consumer_secret == None):
            raise Exception('Error: The Twitter API consumer key or access token has not been set.')

        # Twitter に接続
        self.twitter = twitter.Twitter(auth = twitter.OAuth(
            access_token, access_token_secret, consumer_key, consumer_secret
        ))


    def get_timeline(self, since_id = None, include_rts = False, exclude_replies = False):
        """
        タイムラインを再帰的に取得する
        @param count 取得するツイート数
        @param since_id 指定する ID よりも大きい ID のツイートのみを取得する
        @param include_rts 取得結果にリツイートを含む
        @param exclude_replies 取得結果にリプライを含まない
        @return 取得結果
        """

        if __name__ == '__main__':
            print('Getting tweets ...')

        # 一度に取得するツイート数
        count = 200

        # 初回取得
        if (since_id != None):  # since_id あり
            timeline = self.twitter.statuses.user_timeline(
                tweet_mode = 'extended',
                include_entities = True,
                include_rts = include_rts,
                exclude_replies = exclude_replies,
                screen_name = self.screen_name,
                count = count,
                since_id = int(since_id),
            )
        else:  # since_id なし
            timeline = self.twitter.statuses.user_timeline(
                tweet_mode = 'extended',
                include_entities = True,
                include_rts = include_rts,
                exclude_replies = exclude_replies,
                screen_name = self.screen_name,
                count = count,
            )
        max_id = timeline[-1]['id']

        while True:

            # 1秒待機
            time.sleep(1)

            if __name__ == '__main__':
                print('Getting tweets ...')

            # 指定されたユーザーのタイムラインを取得
            if (since_id != None):  # since_id あり
                result = self.twitter.statuses.user_timeline(
                    tweet_mode = 'extended',
                    include_entities = True,
                    include_rts = include_rts,
                    exclude_replies = exclude_replies,
                    screen_name = self.screen_name,
                    max_id = max_id,
                    count = count,
                    since_id = int(since_id),
                )
            else:  # since_id なし
                result = self.twitter.statuses.user_timeline(
                    tweet_mode = 'extended',
                    include_entities = True,
                    include_rts = include_rts,
                    exclude_replies = exclude_replies,
                    screen_name = self.screen_name,
                    max_id = max_id,
                    count = count,
                )

            # ツイートが 1 個だけだったらループを抜ける
            if len(result) == 1:
                break

            # リストに追加
            # 0番目は max_id のツイート自身が含まれているので除外
            timeline.extend(result[1:])

            # max_id を設定
            max_id = result[-1]['id']

        return timeline


    def get_statuses_count(self):
        """
        ツイート数を取得する
        @return 取得結果
        """

        # 指定されたユーザーのツイート数を取得する
        result = self.twitter.users.lookup(
            screen_name = self.screen_name,
            exclude_replies = False,
        )

        return int(result[0]['statuses_count'])


    # 参考: https://github.com/yuitest/twitterxauth/blob/master/twitterxauth/__init__.py
    def get_oauth_tokens(self, consumer_key, consumer_secret, screen_name, password,
        API_URL = 'https://api.twitter.com/oauth/access_token'):

        consumer = oauth2.Consumer(consumer_key, consumer_secret)
        client = oauth2.Client(consumer)
        client.add_credentials(screen_name, password)
        client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        _, token = client.request(
            API_URL, method='POST', body=urllib.parse.urlencode({
                'x_auth_mode': 'client_auth',
                'x_auth_username': screen_name,
                'x_auth_password': password,
            }))
        parsed_token = dict(urllib.parse.parse_qsl(token))
        return (parsed_token['oauth_token'], parsed_token['oauth_token_secret'])


if __name__ == '__main__':

    # 引数チェック
    param = sys.argv
    if (len(param) != 2):
        print(('Usage: $ python ' + param[0] + ' @screenname'))
        exit()


    # クラスを初期化
    instance = PassTweetstoText(param[1])

    print('Screen name: ' + instance.screen_name)

    # ユーザーのツイート数を取得
    statuses_count = instance.get_statuses_count()

    # ユーザーの全ツイートを再帰的に取得
    timeline = instance.get_timeline(include_rts = True)

    for index, tweet in enumerate(timeline):
        print('Tweet ' + str(index + 1) + ' (' + tweet['id_str'] + '): ' + tweet['full_text'])

    print('Number of tweets: ' + str(statuses_count))
    print('Number of tweets got: ' + str(len(timeline)))


    

