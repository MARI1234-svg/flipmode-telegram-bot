from flask import Flask, request
import telegram
from polygon_checker import check_trade_result

app = Flask(__name__)

# FlipModeBot token with /check command
TOKEN = "7905913196:AAHcfq9dAczcM8L-xyrY9vhsjPNzSPL_6dQ"
bot = telegram.Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/check"):
            try:
                _, ticker, strike, expiry, option_type = text.split()
                result = check_trade_result(ticker, strike, expiry, option_type)
                bot.send_message(chat_id=chat_id, text=result)
            except Exception as e:
                bot.send_message(
                    chat_id=chat_id,
                    text=f"❌ Format error. Use:
/check TICKER STRIKE YYYY-MM-DD CALL|PUT\nError: {e}"
                )
        else:
            bot.send_message(
                chat_id=chat_id,
                text="🤖 Send:
/check TICKER STRIKE YYYY-MM-DD CALL|PUT"
            )

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)