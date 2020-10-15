
# TextGeneratorPlus

マルコフ連鎖を使った文章自動生成プログラムです。  
Python3 に対応しているほか、以下の変更を行っています。

- 動くか微妙で需要もなさそうなはてなブログ投稿スクリプトを削除

## 環境

Windows 10 64bit の Python 3.7.7 で動作を確認しています。  
それ以外の環境でも Python3 が入っていて、MeCab を動かすことができれば動作するはずです。

## インストール

以下のコマンドを実行してください。  
Windows 64bit で実行している場合は、別途 [こちら](https://github.com/ikegami-yukino/mecab/releases) から 64bit 版 MeCab のインストールが必要です。

~~~~
$ pip install mecab
$ git clone https://github.com/nkutomi/TextGenerator.git
$ cd TextGenerator
~~~~

## 使い方

### 事前準備

事前準備として、適当な長い文章が入ったテキストデータを用意します。 ex: `sample.txt`  
以下のコマンドを実行し、事前準備を実行します。

もし実行途中で RuntimeError が出てしまっている場合は、何らかの原因で MeCab の実行に失敗しています。  
MeCab の実行には [こちら](https://qiita.com/yukinoi/items/990b6933d9f21ba0fb43) のラッパーを利用します。  
前述の通り、Windows 64bit で実行している場合は 64bit 版の MeCab が実行できる状態にしておいてください。

~~~~
$ python PrepareChain.py samples/sample.txt 
~~~~

なお、sample.txt 以外にも夏目漱石の小説を 5 つ入れてあり、5 つを 1 つのファイルにまとめた souseki_all5.txt もあります。  
これは青空文庫（https://www.aozora.gr.jp/index_pages/person148.html#sakuhin_list_1 ）から旧字やルビなどの削除といった加工を行ったものです。  
sample.txt と比べ文章数が多いため、事前準備と生成に少し時間がかかります。

### 文章の生成

事前準備を実施したあと、以下のコマンドを実行します。
引数は文章の数を表します。以下は文章数が 10 のときの例です。

~~~~
$ python GenerateText.py 10
~~~~

リダイレクトを利用することで、ファイルに出力することもできます。

~~~~
$ python GenerateText.py 10 > output.txt
~~~~

## ファイル構成

### README.md
このファイル

### PrepareChain.py
適当なテキストを与えて、そこから 3 つ組のチェーンを作成し、DB に保存するファイル

### GenerateText.py
実際にランダムで文章を生成するファイル

### schema.sql
DB 作成のためのスキーマファイル

### chain.db
Git で管理はされていないが、3 つ組チェーンの情報が保存されているDBファイル

## バージョン

ver 0.1 base karaage modify version, modified for python 3 by nkutomi
