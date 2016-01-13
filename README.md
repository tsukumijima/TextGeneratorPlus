# Text Generator
マルコフ連鎖を使った文章自動生成プログラム

## バージョン
ver 0.1 base karaage modify version

## 使い方
文章の自動生成の方法

### 事前準備
まずは、事前準備として、適当な長い文章が入ったテキストデータを用意 ex:'sample txt'
以下コマンド実行
~~~~
$ python PrepareChain.py sample.txt 
~~~~

### 文章の生成
事前準備がされていることが前提

~~~~
$ python GenerateText.py
~~~~


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
