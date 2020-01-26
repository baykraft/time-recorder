import os

# SlackのAPIを利用するためのトークン
# アプリとして追加した「Hubot」のトークンを貼り付ける
API_TOKEN = os.environ.get('BOT_API_TOKEN')

# 対応するメッセージがなかった場合に反応するメッセージ
DEFAULT_REPLY = "I don't understand you."

# Botが実行するスクリプトを配置するディレクトリパスのリスト
PLUGINS = ['plugins']
