import random
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 1. LINEの設定（LINE Developersで取得したものを貼り付けます）
CHANNEL_ACCESS_TOKEN = 'qXXlZM9/GujYKM7HWj04ZBxr9khggOV8pDr1p5+sIMclwcRrXKnikE3/sCGRAaEx8aF2FhueL2LNmXp4Y4M8Fh6LgP9XM+nVlds2rrCjzpNb3Zf8OwIaWsKDH3R3DZwG8D9dymhk65OPhVXbUHPOOgdB04t89/1O/w1cDnyilFU='
MY_USER_ID = 'U4e60a88e1bd964973017b462079665c6'

# 2. 占いのロジック（まずはシンプルに3つの運勢からランダムで選ぶ）
fortunes = [
    "今日の運勢は【大吉】！最高の1日になりそうです。ラッキーアイテムはコーヒー☕️",
    "今日の運勢は【中吉】！一歩一歩進めば良いことがあります。ラッキーカラーは青色💙",
    "今日の運勢は【小吉】！のんびりマイペースにいきましょう。ラッキーフードはリンゴ🍎"
]
today_fortune = random.choice(fortunes)

# 3. LINEに送信する
try:
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(MY_USER_ID, TextSendMessage(text=today_fortune))
    print("LINEに占いを送信しました！スマホを確認してみてね。")
except Exception as e:
    print(f"エラーが発生しました: {e}")