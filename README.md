
# TweetGenerator

マルコフ連鎖を使ったツイート自動生成プログラムです。  
Python3 に対応しているほか、本家やそのフォークと比べ、以下の変更を行っています。

- ランダムに 140 文字以内の文章を生成し、ツイートする Tweet.py を追加
- アカウントの過去のツイートを遡って全て取得し本文をテキストファイルに出力する PastTweettoText.py を追加
- アカウントのアクセストークンとアクセストークンシークレットを xAuth で取得する TwitterXAuth.py を追加
- Twitter API を操作するクラス TwitterAPI と ユーティリティークラス Utils を追加
- ツイート用途では不要なはてなブログ投稿スクリプトを削除

## 環境

Windows 10 64bit の Python 3.7.7 で動作を確認しています。  
それ以外の環境でも Python3 が入っていて、MeCab を動かすことができれば動作するはずです。

## インストール

以下のコマンドを実行してください。  
Windows 64bit で実行している場合は、別途 [こちら](https://github.com/ikegami-yukino/mecab/releases) から 64bit 版 MeCab のインストールが必要です。

~~~~
$ pip install mecab oauth2 python-dotenv twitter
$ git clone https://github.com/tsukumijima/TweetGenerator.git
$ cd TweetGenerator
~~~~

## 使い方

### アクセストークンの設定

Twitter API でツイートを検索したりツイートしたりするためには、コンシューマーキー (CK)・コンシューマーシークレット (CS)・  
アクセストークン (AT)・アクセストークンシークレット (ATS) の 4 つの鍵が必要になります。

ただし、通常の Twitter API の検索では、1週間より前のツイートを取得することができません。  
アカウントごとのツイートも最大で 3200 件までしか取得できない、という制限があり、後述する指定したアカウントの過去のツイート全てを取得することは不可能です。

そこで、このプログラムでは、通常の Twitter API アプリには公開されていない、非公開の Twitter API (search/universal) を使ってツイートを取得します。  
search/universal は TweetDeck などで利用されている非公開 API で、Twitter for Android など、公式の CK/CS を認証に使うことで利用できます。  
非公式の方法になるため、（ないとは思いますが）場合によってはアカウントが BAN されたりする可能性もあります。実行は自己責任のもとでお願いします。  

アクセストークンの設定は .env で行います。.env.example を .env にコピーし、内容を編集してください。

#### コンシューマーキー・コンシューマーシークレット

非公開の Twitter API にアクセスするため、前述の通り CK/CS は公式のものを利用します。  
それぞれ Android 用、iPhone 用どちらか一つをコメントアウトして設定してください（ CK は Android・CS は iPhone のような組み合わせは不可）。  
他の公式 CK/CS を設定することもできますが、通常の手段で入手したコンシューマーキーを設定すると動作しません。

「Login denied due to suspicious activity. Please check your email for further login instructions.」というエラーが表示される場合は、  
しばらく xAuth ができない状態になってしまっています。他のアカウントを使うか、解除されるまで待ちましょう。  
一度不審と判断されてしまうと、少なくとも数時間は xAuth ができない状態になるようです。できれば、普段使っている方のクライアントの公式 CK/CS を選択した方がよいでしょう。  
Twitter for Android の方が成功率が高そうなので、そちらをデフォルトにしています。このあたりはすごく微妙ですが、一度トークンが取得できればずっと利用できるようです。

#### アクセストークン・アクセストークンシークレット

~~~~
$ python TwitterXAuth.py
Screen name: (スクリーンネームを入力)
Password: (パスワードを入力)
Access token       : YOUR_ACCESS_TOKEN
Access token secret: YOUR_ACCESS_TOKEN_SECRET
~~~~

公式の CK/CS を利用するため、ログイン方式も OAuth ではなく、xAuth というアカウント名とパスワードでログインする特殊な方式で行います。  
あらかじめ上記の設定を行ったうえで、上記のように `python TwitterXAuth.py` と実行し、プロンプトでアカウント名とパスワードを入力します。  
認証に成功すればアクセストークンとアクセストークンシークレットが表示されるので、それを下記にコピペしてください。

xAuth 認証は実行しすぎると不審と判断され、最悪しばらく xAuth ができなくなってしまったり、凍結してしまう可能性もあります。認証は何回も続けて行わないようにしてください。  
非公式の方法なので、認証の実行は自己責任のもとでお願いします。念のため、凍結しても問題ないアカウントで実行することを推奨します。

### 事前準備

事前準備として、適当な長い文章が入ったテキストデータを用意します。 ex: `sample.txt`  
以下のコマンドを実行し、事前準備を実行します。

もし実行途中で RuntimeError が出てしまっている場合は、何らかの原因で MeCab の実行に失敗しています。  
MeCab の実行には [こちら](https://qiita.com/yukinoi/items/990b6933d9f21ba0fb43) のラッパーを利用します。  
前述の通り、Windows 64bit で実行している場合は 64bit 版の MeCab が実行できる状態にしておいてください。

~~~~
$ python PrepareChain.py samples/sample.txt
~~~~

#### 夏目漱石の小説を利用する

なお、sample.txt 以外にも夏目漱石の小説を 5 つ入れてあり、5 つを 1 つのファイルにまとめた souseki_all5.txt もあります。  
これは、青空文庫（https://www.aozora.gr.jp/index_pages/person148.html#sakuhin_list_1 ）から旧字やルビなどの削除といった加工を行ったものです。

sample.txt と比べ文章数が多いため、事前準備と生成に少し時間がかかります。

#### 指定アカウントの過去ツイートを利用する

~~~~
$ python PastTweetstoText.py @AbeShinzo
~~~~

上記のように PastTweetstoText.py を実行することで、引数に指定したスクリーンネームのアカウントの過去のツイートを遡って全て取得し、  
ツイート本文を改行・ハッシュタグ・メンション・URL の削除などの加工を行った上で 1 ツイートごとに改行し、pasttweets/(スクリーンネーム).txt に保存します。

スクリーンネームは @ があってもなくても構いませんが、PowerShell では @ が特殊文字扱いなので注意してください（ ` でエスケープできます）。

~~~~
$ python PrepareChain.py pasttweets/AbeShinzo.txt
~~~~

その後、書き出したテキストファイルを事前準備で利用すれば、指定したアカウントの過去ツイートから文章を生成することができます。

### 文章の生成

事前準備を実施したあと、以下のコマンドを実行できます。
引数は文章の数を表します。以下は文章数が 10 のときの例です。

~~~~
$ python GenerateText.py 10
~~~~

リダイレクトを利用することで、ファイルに出力することもできます。

~~~~
$ python GenerateText.py 10 > output.txt
~~~~

### ツイートを送信する

~~~~
$ python Tweet.py
~~~~

GenerateText.py で文章が生成できていることを確認したら、生成した文章をつかってツイートしてみましょう。  
140 文字以内の文章がランダムで生成され、以前 xAuth で認証したアカウントにてツイートされます。　　
あとは Cron でこのコマンドを定期的に実行されるようにしておけば、Twitter でおなじみの Bot の完成です。

## ファイル構成

実際に実行するファイルは以下の 5 つで構成されています。  
それ以外のファイルは設定ファイルやクラス、データベースなどです。

### TwitterXAuth.py
アカウントのアクセストークンとアクセストークンシークレットを xAuth で取得するファイル

### PastTweetstoText.py
search/universal で指定されたアカウントの過去のツイートを遡って全て取得し、pasttweets/ 以下に (アカウント名).txt という名前で保存するファイル

### PrepareChain.py
適当なテキストを与えて、そこから 3 つ組のチェーンを作成し、DB に保存するファイル

### GenerateText.py
実際にランダムで文章を生成するファイル

### Tweet.py
ランダムに 140 文字以内の文章を生成し、ツイートするファイル

----

### TwitterAPI.py
Twitter API を操作するクラスファイル

### Utils.py
ユーティリティークラスファイル

----

### .env
Git で管理はされていないが、環境設定が書かれているファイル

### .env.example
.env の雛形となるファイル

### chain.db
Git で管理はされていないが、3 つ組チェーンの情報が保存されているDBファイル

### schema.sql
DB 作成のためのスキーマファイル

### README.md
このファイル

## バージョン

ver 0.1 base karaage modify version, modified for python 3 by nkutomi
