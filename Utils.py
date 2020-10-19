# -*- coding: utf-8 -*-

"""
ユーティリティークラス
"""

import os
import re


class Utils:

    @staticmethod
    def remove_hashtag(string):
        """
        文章からハッシュタグを削除する
        @param string 文字列
        @return ハッシュタグを削除した文字列
        """
        return re.sub(r'(#[^\s]+)', '', string).strip()

    @staticmethod
    def remove_mention(string):
        """
        文章からメンションを削除する
        @param string 文字列
        @return メンションを削除した文字列
        """
        return re.sub(r'(@[^\s]+)', '', string).strip()

    @staticmethod
    def remove_url(string):
        """
        文章から URL を削除する
        @param string 文字列
        @return URL を削除した文字列
        """
        return re.sub(r'(https?://[^\s]+)', '', string).strip()

    @staticmethod
    def file_get_contents(path):
        """
        ファイルを読み込む
        @param path ファイルのパス
        @return ファイルの内容
        """
        if os.path.isfile(path):
            with open(path, 'r') as file:
                contents = file.read()
                return contents

    @staticmethod
    def file_put_contents(path, contents):
        """
        ファイルに書き込む
        @param path ファイルのパス
        @return 書き込んだファイルのバイト数
        """
        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'w') as file:
            file.write(contents)
        return os.path.getsize(path)
