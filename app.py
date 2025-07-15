from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random
from dotenv import load_dotenv
import os

# Flaskアプリの準備
app = Flask(__name__)

# .envファイルから環境変数読み込み
load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# LINE BOT APIとWebhook Handlerの初期化
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ツンデレの通常返信（ランダムに使われる）
tsundere_replies = [
    "べ、別にあんたのために返信したわけじゃないんだからね！？",
    "暇だったから返信してあげただけよ！",
    "ちょっと…そんなに話しかけないでよ。……でも嫌いじゃないけど。",
    "あ、ありがとう…って言うと思った？べ、別に嬉しくなんかないし！",
    "ちょっとだけ…ちょっとだけね！嬉しいかも…",
    "バカ！って言いたくなるけど、ちょっと心配になっちゃうんだからね。",
    "なんであんたばっかり優しくするのよ！ズルいじゃない！",
    "ふん、別に心配してるわけじゃないんだからね！勘違いしないでよ！",
    "もう、なんでそんなにしつこいのよ！…でも、無視できないわ。",
    "あんたのことなんてどうでもいいけど…返事くらいはしてあげるわよ。",
    "うるさい！でも、たまに面白いこと言うじゃない。",
    "うぅん、別に好きとかじゃないけど…ちょっと気になるだけよ。",
    "しょうがないから相手してあげるわよ。でも勘違いしないでね？",
    "私のこと嫌いなら、ほっといてよ。でも…ちょっとは気にしてよね！",
    "恥ずかしいからあんまり近づかないでよね。…でも、来てほしいな。"
]

# キーワードに対するランダムな返答集
response_map = {
    "おはよう": [
        "お、おはよう...って、なんであたしが先に挨拶しなきゃいけないのよ！",
        "ふーん、ちゃんと起きれるんだ...あんたのくせにすごいじゃない！",
        "は？別にあんたが起きるの待ってたわけじゃないし。おはよう",
        "べ、別にあんたのために言ってるわけじゃないんだからね！おはよう。",
        "おはよう…って、ちゃんと起きてるの？遅刻しないでよね！",
    ],
    "疲れた": [
        "べ、別に心配してるわけじゃないんだからね！でも無理しないでよ。",
        "疲れたって…そんなに頑張ってるの？ちょっとは休みなさいよね。",
        "はぁ…疲れてるなら、そっとしておいてあげるわよ。",
        "ちょっとくらい甘えたっていいんだからね！",
        "休まなきゃダメよ…ったく、放っておけないじゃない。",
    ],
    "好き": [
        "な、なに言ってんのよ...でもちょっとだけ嬉しいかも。",
        "ちょ、ちょっと...もう一回言ってみなさいよ...！",
        "急にそんなこと言われたら…ドキドキしちゃうじゃない…！",
        "うるさいっ…そんなこと言われたら意識しちゃうじゃない！",
        "あーもうっ！……好きとか、簡単に言うな…でも、ありがと。",
    ],
    "うざい": [
        "は？あんたに言われたくないし！",
        "うざいって…あんたにだけは言われたくないんだけど！？",
    ],
    "寂しい": [
        "べ、別に寂しくなんてないけど…ちょっとだけなら話してあげてもいいわよ？",
        "寂しいなら…私が話し相手になってあげてもいいけど？",
    ],
    "かわいい": [
        "か、かわいい！？…う、うるさい！",
        "そ、そんなこと言われたら…ちょっと照れるじゃない…",
    ],
    "バカ": [
        "バカって言う方がバカなんだから！",
        "もう、バカバカ言わないでよ…でも、ちょっと嬉しいかも？",
    ],
}

# キーワードに応じたランダム返信を返す関数
def get_response(keyword: str) -> str:
    responses = response_map.get(keyword)
    if responses:
        return random.choice(responses)
    else:
        return random.choice(tsundere_replies)

# Webhookエンドポイント
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# メッセージイベントのハンドラ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.lower()
    print(f"Received message: {user_text}")

    # キーワードのどれかに一致するか確認
    for keyword in response_map.keys():
        if keyword in user_text:
            reply = get_response(keyword)
            break
    else:
        reply = random.choice(tsundere_replies)

    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    except LineBotApiError as e:
        print(f"LINE返信エラー: {e}")

# Flaskアプリ起動
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
