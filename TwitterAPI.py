# -*- coding: utf-8 -*-

"""
Twitter API を操作するクラス
"""

import os
import time

import dotenv
import twitter

# Windows 環境向けの hack
# 参考: https://stackoverflow.com/questions/31469707/changing-the-locale-preferred-encoding-in-python-3-in-windows
if os.name == 'nt':
    import _locale
    _locale._getdefaultlocale_backup = _locale._getdefaultlocale
    _locale._getdefaultlocale = (lambda *args: (_locale._getdefaultlocale_backup()[0], 'UTF-8'))


class TwitterAPI:

    def __init__(self):

        # .env を読み込み
        dotenv.load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '/.env')

        # Twitter API の各種キーを取得
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')

        # 各種キーのいずれかが取得できなかったらエラー
        if (access_token is None or access_token_secret is None or
            consumer_key is None or consumer_secret is None):
            raise Exception('The Twitter API consumer key or access token has not been set.')

        # 参考: https://github.com/TwidereProject/Twidere-Android/blob/master/twidere/src/main/kotlin/org/mariotaku/twidere/util/api/TwitterAndroidExtraHeaders.kt
        # User-Agent で TwitterAndroid を指定するのが重要、ほかは指定しなくてもツイートできるけど念のため
        headers = {
            'Accept-Language': 'ja',
            'User-Agent': 'TwitterAndroid/6.41.0 (7160062-r-930) Pixel 3a/10 (Google;Pixel 3a;google;sargo;0;;0)',
            'X-Twitter-Client': 'TwitterAndroid',
            'X-Twitter-Client-Language': 'ja',
            'X-Twitter-Client-Version': '6.41.0',
            'X-Twitter-API-Version': '5',
        }
        twitter.OAuth.generate_headers = (lambda *args: headers)

        # Twitter に接続
        self.twitter = twitter.Twitter(auth = twitter.OAuth(
            access_token, access_token_secret, consumer_key, consumer_secret
        ))

    def get_user_timeline(self, screen_name, since_id = None, include_rts = False, include_replies = True):
        """
        search/universal を使いアカウントのタイムラインを再帰的に取得する
        @param screen_name アカウントのスクリーンネーム
        @param count 取得するツイート数
        @param since_id 指定する ID よりも大きい ID のツイートのみを取得する
        @param include_rts 取得結果にリツイートを含む
        @param include_replies 取得結果にリプライを含む
        @return 取得結果
        """

        # 一度に取得するツイート数
        count = 100  # 100 個が最大らしい（このうち1個は max_id で指定したツイート自身なので実質 99 個）

        # 検索クエリを作成
        query = f'from:@{screen_name} '
        if include_rts is True:
            query += 'include:nativeretweets '
        else:
            query += 'exclude:nativeretweets '
        if include_replies is True:
            query += 'include:replies '
        else:
            query += 'exclude:replies '
        if since_id is not None:
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

            # 指定されたアカウントのタイムラインを取得
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

    def get_user_tweets_count(self, screen_name):
        """
        アカウントのツイート数を取得する
        @param screen_name アカウントのスクリーンネーム
        @return 取得結果
        """

        # 指定されたアカウントのツイート数を取得する
        result = self.twitter.users.lookup(
            screen_name = screen_name,
            exclude_replies = False,
            tweet_mode = 'extended',
        )

        return int(result[0]['statuses_count'])

    def tweet(self, message):
        """
        ツイートを送信する
        @param message ツイート本文
        @return ツイート結果
        """

        result = self.twitter.statuses.update(
            status = message,
            tweet_mode = 'extended',
        )

        return result
