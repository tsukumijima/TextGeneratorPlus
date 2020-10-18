# -*- coding: utf-8 -*-

"""
search/universal で指定されたアカウントの過去のツイートを遡って全て取得し、
pasttweets 以下に (アカウント名).txt という名前で保存するファイル
"""

import math
import os
import re
import sys
import time

import dotenv
import twitter

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
            raise Exception('The Twitter API consumer key or access token has not been set.')

        # Twitter に接続
        self.twitter = twitter.Twitter(auth = twitter.OAuth(
            access_token, access_token_secret, consumer_key, consumer_secret
        ))


    def get_user_timeline(self, since_id = None, include_rts = False, include_replies = True):
        """
        search/universal を使いユーザーのタイムラインを再帰的に取得する
        @param count 取得するツイート数
        @param since_id 指定する ID よりも大きい ID のツイートのみを取得する
        @param include_rts 取得結果にリツイートを含む
        @param include_replies 取得結果にリプライを含む
        @return 取得結果
        """

        # 一度に取得するツイート数
        count = 100  # 100 個が最大らしい（このうち1個は max_id で指定したツイート自身なので実質 99 個）

        # 検索クエリを作成
        query = f'from:@{self.screen_name} '
        if include_rts == True:
            query += 'include:nativeretweets '
        else:
            query += 'exclude:nativeretweets '
        if include_replies == True:
            query += 'include:replies '
        else:
            query += 'exclude:replies '
        if since_id != None:
            query += f'since_id:{since_id} '


        # 初回取得
        if __name__ == '__main__':
            print('Getting tweets ...')

        user_timeline = self.twitter.search.universal(
            q = query,
            count = count,
            result_type = 'recent',
            tweet_mode = 'extended',
            modules = 'status',
        )['modules']
        
        # max_id を設定
        max_id = user_timeline[-1]['status']['data']['id_str']

        while True:

            # 0.25秒待機
            time.sleep(0.25)

            if __name__ == '__main__':
                print('Getting tweets ... ' + str(len(user_timeline)).rjust(3, ' ') + ' tweets (max_id:' + max_id + ')')

            # 指定されたユーザーのタイムラインを取得
            result = self.twitter.search.universal(
                q = query + f'max_id:{max_id}',
                count = count,
                result_type = 'recent',
                tweet_mode = 'extended',
                modules = 'status',
            )['modules']

            # ツイートが 1 個だけだったらループを抜ける
            if len(result) == 1:
                break

            # リストに追加
            # 0番目は max_id のツイート自身が含まれているので除外
            user_timeline.extend(result[1:])

            # max_id を設定
            max_id = user_timeline[-1]['status']['data']['id_str']

        return user_timeline


    def get_statuses_count(self):
        """
        ユーザーのツイート数を取得する
        @return 取得結果
        """

        # 指定されたユーザーのツイート数を取得する
        result = self.twitter.users.lookup(
            screen_name = self.screen_name,
            exclude_replies = False,
        )

        return int(result[0]['statuses_count'])


    @staticmethod
    def remove_hashtag(string):
        """
        ツイート本文からハッシュタグを除去する
        @param string 文字列
        @return ハッシュタグを除去した文字列
        """
        return re.sub(r'(#[^\s]+)', '', string).strip()

    @staticmethod
    def remove_mention(string):
        """
        ツイート本文からメンションを除去する
        @param string 文字列
        @return メンションを除去した文字列
        """
        return re.sub(r'(@[^\s]+)', '', string).strip()

    @staticmethod
    def remove_url(string):
        """
        ツイート本文から URL を除去する
        @param string 文字列
        @return URL を除去した文字列
        """
        return re.sub(r'(https?://[^\s]+)', '', string).strip()

    @staticmethod
    def file_get_contents(path):
        if os.path.isfile(path):
            with open(path, 'r') as file:
                contents = file.read()
                return contents

    @staticmethod
    def file_put_contents(path, contents):
        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'w') as file:
            file.write(contents)
        return os.path.getsize(path)


if __name__ == '__main__':

    # 引数チェック
    param = sys.argv
    if (len(param) != 2):
        print(('Usage: $ python ' + param[0] + ' @screen_name'))
        exit()


    # クラスを初期化
    instance = PassTweetstoText(param[1])

    print('Screen name: @' + instance.screen_name)

    # ユーザーのツイート数を取得
    statuses_count = instance.get_statuses_count()

    # ユーザーの全ツイートを再帰的に取得
    user_timeline = instance.get_user_timeline()

    # ファイルに書き込む
    file_name = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + f'/pasttweets/{instance.screen_name}.txt'
    file_contents = ''
    for index, tweet in enumerate(user_timeline):

        # ツイートの ID と本文
        tweet_id = tweet['status']['data']['id_str']
        tweet_text = tweet['status']['data']['full_text']

        # テキストにするにあたって不要な改行・ハッシュタグ・メンション・URL を除外
        tweet_text_processed = tweet_text.replace('\n', '')
        tweet_text_processed = PassTweetstoText.remove_hashtag(tweet_text_processed)
        tweet_text_processed = PassTweetstoText.remove_mention(tweet_text_processed)
        tweet_text_processed = PassTweetstoText.remove_url(tweet_text_processed)

        # 追記する
        file_contents += tweet_text_processed + '\n'

        print('Tweet ' + str(index + 1) + ' (ID:' + tweet_id + '): ' + tweet_text)

    # ツイート数
    print('Number of tweets: ' + str(statuses_count))
    print('Number of tweets got: ' + str(len(user_timeline)))

    # ファイルを書き込む
    PassTweetstoText.file_put_contents(file_name, file_contents.rstrip('\n'))  # 最後の改行を除去
    print('Saved tweets: ' + file_name)

