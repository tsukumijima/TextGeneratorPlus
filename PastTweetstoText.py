# -*- coding: utf-8 -*-

"""
search/universal で指定されたアカウントの過去のツイートを遡って全て取得し、
pasttweets/ 以下に (アカウント名).txt という名前で保存するファイル
"""

import os
import sys

from TwitterAPI import TwitterAPI
from Utils import Utils

if __name__ == '__main__':

    # 引数チェック
    param = sys.argv
    if (len(param) != 2):
        print(('Usage: $ python ' + param[0] + ' @screen_name'))
        exit()

    # スクリーンネームを設定
    screen_name = param[1].replace('@', '')
    print('Screen name: @' + screen_name)

    # クラスを初期化
    instance = TwitterAPI()

    # アカウントのツイート数を取得
    user_tweets_count = instance.get_user_tweets_count(screen_name)

    # アカウントの全ツイートを再帰的に取得
    user_timeline = instance.get_user_timeline(screen_name)

    # ファイルに書き込む
    file_name = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + f'/pasttweets/{screen_name}.txt'
    file_contents = ''
    for index, tweet in enumerate(user_timeline):

        # ツイートの ID と本文
        tweet_id = tweet['status']['data']['id_str']
        tweet_text = tweet['status']['data']['full_text']

        # テキストにするにあたって不要な改行・ハッシュタグ・メンション・URL を削除
        tweet_text_processed = tweet_text.replace('\n', '')
        tweet_text_processed = Utils.remove_hashtag(tweet_text_processed)
        tweet_text_processed = Utils.remove_mention(tweet_text_processed)
        tweet_text_processed = Utils.remove_url(tweet_text_processed)

        # 追記する
        file_contents += tweet_text_processed + '\n'

        print('Tweet ' + str(index + 1) + ' (ID:' + tweet_id + '): ' + tweet_text)

    # ツイート数
    print('Number of tweets: ' + str(user_tweets_count))
    print('Number of tweets got: ' + str(len(user_timeline)))

    # ファイルを書き込む
    Utils.file_put_contents(file_name, file_contents.rstrip('\n'))  # 最後の改行を除去
    print('Saved tweets: ' + file_name)

