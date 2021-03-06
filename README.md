ナイーブベイズで中二病判定
==========================

## What's this?
中二病なセリフを学習し、入力されたセリフが中二病かどうかを判定してくれるアプリケーションです。

## つかいかた

```
$cd src
$python3 classifier.py
Training...
Training...
input =>僕に勝つのはまだ早いよ
中二病

input =>打ち返せない球はないよ
中二病

input =>あなたは中二病ですか？
中二病ではない

input =>俺は中二病なんぞではない！
中二病

input =>exit
```

実行すると学習結果が```model.json```というファイルに出力されます。  

ファイル名を引数として渡すと、保存された学習結果を利用することができます。

```
$python3 classifier.py model.json
```

## 環境設定
### パッケージのインストール
Ubuntuの場合は予め

```
sudo apt-get install -y libxml2-dev libxslt1-dev
```

としておいてください。  

Twitter APIとbeautifulsoupをインストールします。

```
sudo pip3 install twitter beautifulsoup4 lxml numpy
```

### 設定ファイルの記述
1. [Twitterの開発者用ページ](https://apps.twitter.com/)にアクセスしてTwitter APIのAccess Tokenを発行してください。
2. [Yahoo デベロッパーネットワーク](https://e.developer.yahoo.co.jp/register)にアクセスして形態素解析APIを利用するためのアプリケーションIDを発行してください。
3. 取得したAccess TokenとアプリケーションIDを`src/settings.cfg`に書き込みます。
4. 中二病なツイートをしているアカウントをいくつか探し、そのIDを`src/settings.cfg`のtrue_accountsに設定します。
5. 中二病でないツイートをしているアカウントをfalse_accountsに設定します。

```
[YAHOO]
# YahooのアプリケーションID
appid = 'your yahoo app id'

[TWITTER]
consumer_key = 'your consumer key'
consumer_secret = 'your consumer secret'

token = 'your access token'
token_secret = 'your access token secret'

true_target_name = '中二病'
# 中二病なセリフをツイートしているアカウントのID
true_accounts = ['true_account_id1','true_account_id2']

false_target_name = '中二病ではない'
# 普通のアカウントのID (自分のアカウントなど自由に設定してください)
false_accounts = ['false_account_id1','false_account_id2']
```

以上で設定は終了です。
