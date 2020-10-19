# -*- coding: utf-8 -*-

"""
ランダムに 140 文字以内の文章を生成し、ツイートするファイル
"""

import random

from GenerateText import GenerateText
from TwitterAPI import TwitterAPI

if __name__ == '__main__':

    # 初期化
    generator = GenerateText()
    tweet = TwitterAPI()

    while True:

        # 生成する文章の数
        generator.number = random.randint(2, 6)  # 2文～6文

        # 文章を紡ぐ
        text = generator.generate()

        # 140 文字以下ならループを抜ける
        if len(text) <= 140:
            break


    # ツイートを送信
    print('Tweet: ' + text)
    
    result = tweet.tweet(text)
    print('Tweet ID: ' + result['id_str'])

    print(result)
