import os
from datetime import datetime
import random
from linebot import LineBotApi
from linebot.models import TextSendMessage

# ==========================================
# 1. 各種設定（環境変数 / GitHub Secrets から安全に取得）
# ==========================================
# 【安全性向上】大切な情報はすべてプログラムの外（シークレット）からのみ取得します
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
MY_USER_ID = os.getenv('MY_USER_ID')

# 生年月日（未設定の場合は、エラーを防ぐために仮の「1998-10-15」を使います）
birth_date_str = os.getenv('BIRTH_DATE', '1998-10-15')

# ==========================================
# 2. 数秘術（ヌメロロジー）の計算ロジック
# ==========================================
def get_single_digit_sum(number_str):
    """数字の文字列を受け取り、1桁になるまで（11, 22, 33は残す）各桁を足し算する"""
    while len(number_str) > 1:
        if number_str in ["11", "22", "33"]:
            return int(number_str)
        total = sum(int(digit) for digit in number_str if digit.isdigit())
        number_str = str(total)
    return int(number_str)

def calculate_personal_day_number(birth_str, target_date):
    """生年月日と指定日の日付から、その日の「個人サイクル数」を計算する"""
    try:
        # YYYY-MM-DD の形式を読み込む
        birth = datetime.strptime(birth_str, "%Y-%m-%d")
    except Exception:
        # 万が一、シークレットの登録形式が違った場合のセーフティ
        birth = datetime(1998, 10, 15)
    
    # 誕生月 + 誕生日 + 占いたい年の各桁をすべて足す
    year_digits = str(target_date.year)
    month_digits = str(birth.month)
    day_digits = str(birth.day)
    
    personal_year = get_single_digit_sum(year_digits + month_digits + day_digits)
    
    # さらに、占いたい日の「月」と「日」を足す
    target_month_day = str(target_date.month) + str(target_date.day)
    personal_day = get_single_digit_sum(str(personal_year) + target_month_day)
    
    if personal_day > 9:
        personal_day = get_single_digit_sum(str(personal_day))
        
    return personal_day

# 今日の日付で個人サイクルを計算
today = datetime.now()
personal_day_num = calculate_personal_day_number(birth_date_str, today)

# 各数字（1〜9）が持つ「今日のテーマ」
numerology_meanings = {
    1: "【1：スタート・発展】\n新しいことを始めるのに最適な日！直感に従って即行動が吉です。🚀",
    2: "【2：協調・つながり】\n周りの人の意見をじっくり聞くと良い日。思いやりが運気を呼び込みます。🤝",
    3: "【3：表現・楽しむ】\nクリエイティブな才能が開花する日。美味しいものを食べて楽しんで！🎨🍰",
    4: "【4：安定・基礎】\nコツコツ整理整頓や計画を立てるのに向いている日。足元を固めて。🧹📅",
    5: "【5：変化・挑戦】\nいつもと違う道を通るなど、ちょっとした冒険が新しい扉を開く日です。🏃‍♀️✨",
    6: "【6：愛情・奉仕】\n家族や大切な人、そして自分自身をたくさん労わって甘やかしてあげる日。💖🏡",
    7: "【7：休息・内省】\n読書をしたり一人の時間を作ったりして、自分の心を見つめ直すと良い日。📚🧘‍♀️",
    8: "【8：豊かさ・収穫】\nこれまでの努力が形になって現れるパワフルな日。自信を持って進もう！🏆🌟",
    9: "【9：完結・整理】\n不要になったものや考えを手放し、次のサイクルに向けて心を整理する日。🧹✨"
}

today_numerology_message = numerology_meanings.get(personal_day_num, "【穏やかな日】のんびり過ごしましょう。☕️")

# ==========================================
# 3. おみくじ（ランダム）
# ==========================================
fortunes = [
    "今日の運勢は【大吉】！最高の1日になりそうです。ラッキーアイテムはコーヒー☕️",
    "今日の運勢は【中吉】！一歩一歩進めば良いことがあります。ラッキーカラーは青色💙",
    "今日の運勢は【小吉】！のんびりマイペースにいきましょう。ラッキーフードはリンゴ🍎"
]
today_fortune = random.choice(fortunes)

# ==========================================
# 4. メッセージの合体
# ==========================================
final_message = (
    "🔮 ジュリさん専用・今日の運勢鑑定 🔮\n\n"
    f"{today_fortune}\n\n"
    "🔢 【数秘術から届くメッセージ】\n"
    f"{today_numerology_message}"
)

# ==========================================
# 5. LINEに送信する
# ==========================================
# 安全確認：トークンやIDが空っぽの場合は、LINE送信せずに画面表示だけにする（手元でのテスト用）
if not CHANNEL_ACCESS_TOKEN or not MY_USER_ID:
    print("--- [テスト実行モード] ---")
    print("※LINEの接続情報がローカルPCにないため、送信メッセージのプレビューを表示します：\n")
    print(final_message)
    print("\n--------------------------")
    print("GitHubにプッシュすれば、シークレットを使って実際にLINEへ届きます！")
else:
    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        line_bot_api.push_message(MY_USER_ID, TextSendMessage(text=final_message))
        print("LINEに数秘術付きの占いを送信しました！スマホを確認してみてね。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")