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

# 生年月日（未設定の場合は、エラーを防ぐために仮の「1998-10-15」を使います）
birth_date_str = os.getenv('BIRTH_DATE', '1998-10-15')

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
        birth = datetime(1998, 10, 15)
    
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
# 3. 九星気学の計算ロジック
# ==========================================
def calculate_honmei_sei(birth_str):
    """生年月日から「本命星」を計算する（簡易版：立春のズレは考慮せず西暦年で計算します）"""
    try:
        birth = datetime.strptime(birth_str, "%Y-%m-%d")
    except Exception:
        birth = datetime(1998, 10, 15)
    
    year = birth.year
    # 生まれた年の各桁を足し合わせ、1桁になるまで足す
    year_sum = sum(int(digit) for digit in str(year))
    while year_sum >= 10:
        year_sum = sum(int(digit) for digit in str(year_sum))
    
    # 本命星の割り出し（男性・女性共通の簡易式）
    # 西暦の各桁の和を10から引く（引ききれない場合は調整）
    star_num = 11 - year_sum
    if star_num > 9:
        star_num -= 9
    elif star_num < 1:
        star_num += 9
        
    stars = {
        1: "一白水星 (いっぱくすいせい)",
        2: "二黒土星 (じこくどせい)",
        3: "三碧木星 (さんぺきもくせい)",
        4: "四緑木星 (しろくもくせい)",
        5: "五黄土星 (ごおうどせい)",
        6: "六白金星 (ろっぱくきんせい)",
        7: "七赤金星 (しちせききんせい)",
        8: "八白土星 (はっぱくどせい)",
        9: "九紫火星 (きゅうしかせい)"
    }
    return stars.get(star_num, "一白水星 (いっぱくすいせい)")

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
    # 日付の「日」を基準に、毎日違う方位が選ばれるようにする
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
# 4. メッセージの合体（おみくじを廃止し、本命星と吉方位を追加）
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
        print("LINEに「九星気学＆数秘術」占いを送信しました！")
    except Exception as e:
        print(f"エラーが発生しました: {e}")