# CTFtime-DiscordBot
テスト段階です
## 環境
Python 3.11.4 (zoneinfoを使用している関係上、3.9以上が要件です)

`pip install requests`

`pip install discord.py`

## configについて
そのままcloneしただけだと動きません。config_sample.pyの中身のtokenとappidを指定し、config_sample.pyをconfig.pyにリネームしてください。

### token
Botのトークンを指定してください。(Botの作成時に発行されるものです。)

### appid
BotのアプリケーションIDを指定してください。

### owner_id
bot管理者のDiscordアカウントのIDを指定してください。(ユーザー名ではなく、開発者モードで取得できる数字の方のIDです。)