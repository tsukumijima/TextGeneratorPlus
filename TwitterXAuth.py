# -*- coding: utf-8 -*-

"""
アカウントのアクセストークンとアクセストークンシークレットを xAuth で取得するファイル
"""

import os
import sys

import dotenv
import oauth2
import urllib

# Windows 環境向けの hack
# 参考: https://stackoverflow.com/questions/31469707/changing-the-locale-preferred-encoding-in-python-3-in-windows
if os.name == 'nt':
    import _locale
    _locale._getdefaultlocale_backup = _locale._getdefaultlocale
    _locale._getdefaultlocale = (lambda *args: (_locale._getdefaultlocale_backup()[0], 'UTF-8'))


class TwitterXAuth:

    def __init__(self):

        # .env を読み込み
        dotenv.load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '/.env')

        # Twitter API の各種キーを取得
        self.consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        self.consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')

        # 各種キーのいずれかが取得できなかったらエラー
        if (self.consumer_key == None or
            self.consumer_secret == None):
            raise Exception('The Twitter API consumer key or access token has not been set.')


    def xauth(self, screen_name, password, api_url = 'https://api.twitter.com/oauth/access_token'):
        """
        スクリーンネームとパスワードで xAuth を行う
        参考: https://github.com/yuitest/twitterxauth/blob/master/twitterxauth/__init__.py
        @param screen_name スクリーンネーム
        @param password パスワード
        @return アクセストークンとアクセストークンシークレットのタプル
        """

        consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)
        client = oauth2.Client(consumer)
        client.add_credentials(screen_name, password)
        client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        _, token = client.request(
            api_url, method='POST', body=urllib.parse.urlencode({
                'x_auth_mode': 'client_auth',
                'x_auth_username': screen_name,
                'x_auth_password': password,
            }))
        
        parsed_token = dict(urllib.parse.parse_qsl(token))
        if parsed_token == {}:
            raise Exception(token.decode('UTF-8'))

        return (parsed_token[b'oauth_token'].decode('UTF-8'), parsed_token[b'oauth_token_secret'].decode('UTF-8'))


if __name__ == '__main__':

    # 初期化
    instance = TwitterXAuth()

    # スクリーンネームを取得
    screen_name = input('Screen name: ')

    # パスワードを取得
    password = input('Password: ')

    # xAuth を実行
    access_token, access_token_secret = instance.xauth(screen_name, password)

    # アクセストークンとアクセストークンシークレットを表示
    print('Access token       : ' + access_token)
    print('Access token secret: ' + access_token_secret)

