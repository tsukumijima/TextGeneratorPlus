# Text Generator
マルコフ連鎖を使った文章自動生成プログラム

## バージョン
ver 0.1 base karaage modify version

## 使い方
文章の自動生成の方法

### インストール(git clone)

~~~~
$ git clone https://github.com/karaage0703/TextGenerator.git
$ cd TextGenerator
~~~~

### 事前準備
まずは、事前準備として、適当な長い文章が入ったテキストデータを用意 ex:`sample txt`
以下コマンド実行
~~~~
$ python PrepareChain.py sample.txt 
~~~~

### 文章の生成
事前準備を実施した後、以下コマンド実行。
引数は文章の数を表す。以下は文章数が10のときの例

~~~~
$ python GenerateText.py 10
~~~~

ファイルに出力も可能

~~~~
$ python GenerateText.py 10 > output.txt
~~~~

### はてなブログに投稿
`post-hatena.py`の以下の箇所を自身のはてなブログに合わせて修正

~~~~
username = 'username'
password = 'API key'
blogname = 'yourblogname.hatenablog.com'
~~~~

以下ではてなブログに投稿できる。`title.txt` `body.txt`にはそれぞれ記事のタイトルと本文を書いたテキストファイルを入れる

~~~~
$ post-hatena.py title.txt body.txt
~~~~

### はてなブログに自動で連続投稿
以下で実行権限を付与
~~~~
$ chmod 755 post-hatena-script.sh
~~~~

例えば10回連続で投稿するには以下
~~~~
$ ./post-hatena-script 10
~~~~

はてなブログは24時間に100回までしか投稿できないので注意すること


## 各ファイル
### README.md
このファイル

### PrepareChain.py
適当なテキストを与えて、そこから3つ組のチェーンを作成し、DBに保存するファイル

### schema.sql
DB作成のためのスキーマファイル

### GenerateText.py
実際にランダムで文章を生成するファイル

### chain.db
gitで管理はされていないが、3つ組チェーンの情報が保存されているDBファイル
