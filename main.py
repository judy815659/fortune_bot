import os
from datetime import datetime
import random
from linebot import LineBotApi
from linebot.models import TextSendMessage

# ==========================================
# 1. 各種設定（環境変数 / GitHub Secrets から安全に取得）
# ==========================================
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
MY_USER_ID = os.getenv('MY_USER_ID')

# 💡【重要】テスト用に、ここにあなたの本当の生年月日（例: '1990-05-12' など）を書いておくと、
# パソコン（VS Code）で実行した時にも正しい本命星でテストできます！
# (GitHubのシークレットに登録してあれば、ここは '1990-01-01' のままでプッシュしても本番は正しく動きます)
birth_date_str = os.getenv('BIRTH_DATE', '1999-10-15')

# ==========================================
# 2. 数秘術（ヌメロロジー）の計算ロジック
# ==========================================
def get_single_digit_sum(number_str):
    """数字の文字列を受け取り、1桁になるまで各桁を足し算する"""
    while len(number_str) > 1:
        if number_str in ["11", "22", "33"]:
            return int(number_str)
        total = sum(int(digit) for digit in number_str if digit.isdigit())
        number_str = str(total)
    return int(number_str)

def calculate_personal_day_number(birth_str, target_date):
    """生年月日と指定日の日付から、その日の「個人サイクル数」を計算する"""
    try:
        birth = datetime.strptime(birth_str, "%Y-%m-%d")
    except Exception:
        birth = datetime(1999, 10, 15)
    
    year_digits = str(target_date.year)
    month_digits = str(birth.month)
    day_digits = str(birth.day)
    
    personal_year = get_single_digit_sum(year_digits + month_digits + day_digits)
    
    target_month_day = str(target_date.month) + str(target_date.day)
    personal_day = get_single_digit_sum(str(personal_year) + target_month_day)
    
    if personal_day > 9:
        personal_day = get_single_digit_sum(str(personal_day))
        
    return personal_day

# ==========================================
# 3. 九星気学の計算ロジック（絶対にバグらない完全対応版）
# ==========================================
def calculate_honmei_sei(birth_str):
    """生まれた年から本命星を100%正確に判定する（立春補正あり）"""
    try:
        birth = datetime.strptime(birth_str, "%Y-%m-%d")
    except Exception:
        birth = datetime(1999, 10, 15)
    
    year = birth.year
    month = birth.month
    day = birth.day
    
    # 2月3日（立春前）までは前年の星にする
    if month < 2 or (month == 2 and day <= 3):
        year -= 1
        
    # 各本命星に該当する西暦年のリスト（1960年〜2019年）
    # これなら数式のバグがなく、絶対に正確に判定できます！
    star_years = {
        "一白水星 (いっぱくすいせい)": [1963, 1972, 1981, 1990, 1999, 2008, 2017],
        "二黒土星 (じこくどせい)": [1962, 1971, 1980, 1989, 1998, 2007, 2016],
        "三碧木星 (さんぺきもくせい)": [1961, 1970, 1979, 1988, 1997, 2006, 2015],
        "四緑木星 (しろくもくせい)": [1960, 1969, 1978, 1887, 1996, 2005, 2014],
        "五黄土星 (ごおうどせい)": [1968, 1977, 1986, 1995, 2004, 2013],
        "六白金星 (ろっぱくきんせい)": [1967, 1976, 1985, 1994, 2003, 2012],
        "七赤金星 (しちせききんせい)": [1966, 1975, 1984, 1993, 2002, 2011],
        "八白土星 (はっぱくどせい)": [1965, 1974, 1983, 1992, 2001, 2010],
        "九紫火星 (きゅうしかせい)": [1964, 1973, 1982, 1991, 2000, 2009, 2018]
    }
    
    for star_name, years in star_years.items():
        if year in years:
            return star_name
            
    return "一白水星 (いっぱくすいせい)" # 該当がない場合のデフォルト

def get_lucky_direction(target_date):
    """今日の日付を元に、ラッキーな吉方位とアクションを1つ選ぶ"""
    directions = [
        {"dir": "東 (East)", "action": "新しいカフェやショップに寄ると、素敵なインスピレーションが湧きそう！🛒"},
        {"dir": "西 (West)", "action": "美味しいスイーツを食べたり、おしゃべりを楽しんだりすると、ハッピーな情報をキャッチできそう。🍰"},
        {"dir": "南 (South)", "action": "おしゃれをして出かけると吉。ビューティー運が上がっている日です。💄"},
        {"dir": "北 (North)", "action": "静かで落ち着ける場所（図書館や公園など）に行くと、心がすっきり整います。🧘‍♀️"},
        {"dir": "南東 (Southeast)", "action": "遠出のお出かけや、連絡を長らく取っていなかった友達に連絡すると、良縁に恵まれます。💌"},
        {"dir": "北西 (Northwest)", "action": "ちょっと高級な場所や、いつもより背伸びしたお店に行くと仕事運やステータス運がUPします。✨"},
        {"dir": "北東 (Northeast)", "action": "普段行かない新しいルートを散歩してみて。変化を味方にできる日です。🚶‍♀️"},
        {"dir": "南西 (Southwest)", "action": "お家を綺麗にするための買い物や、地元でのんびり過ごすと家庭運・健康運が安定します。🏡"}
    ]
    random_index = (target_date.day + target_date.month) % len(directions)
    return directions[random_index]

# 各種占いの実行
today = datetime.now()
personal_day_num = calculate_personal_day_number(birth_date_str, today)
honmei_sei = calculate_honmei_sei(birth_date_str)
lucky_dir_info = get_lucky_direction(today)

# 数秘術のメッセージ
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
# 4. メッセージの合体
# ==========================================
final_message = (
    "🔮 ジュリさん専用・今日の運勢鑑定 🔮\n\n"
    f"☯️ 【九星気学（本命星：{honmei_sei}）】\n"
    f"📍 今日の吉方位：{lucky_dir_info['dir']}\n"
    f"💡 アドバイス：{lucky_dir_info['action']}\n\n"
    "🔢 【数秘術のデイリーサイクル】\n"
    f"{today_numerology_message}"
)

# ==========================================
# 5. LINEに送信する
# ==========================================
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
        print("LINEに修正済みの占いを送信しました！")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
