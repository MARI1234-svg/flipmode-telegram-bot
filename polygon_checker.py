import requests
from datetime import datetime

API_KEY = "DsVdKqAU7iZVagnjXCMgFmIDRmSuo9th"

def check_trade_result(ticker, strike, expiry, option_type):
    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        url = f"https://api.polygon.io/v1/open-close/{ticker}/{expiry_date}?adjusted=true&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "close" not in data:
            return f"❌ No close data for {ticker} on {expiry_date}."

        close_price = float(data["close"])
        strike = float(strike)

        if option_type.upper() == "CALL":
            result = "WIN" if close_price > strike else "LOSS"
        elif option_type.upper() == "PUT":
            result = "WIN" if close_price < strike else "LOSS"
        else:
            return "❌ Invalid option type. Use CALL or PUT."

        return (
            f"📊 {ticker} {strike}{'C' if option_type.upper() == 'CALL' else 'P'} ({expiry})\n"
            f"📈 Close Price: ${close_price:.2f} | 🎯 Strike: ${strike}\n"
            f"{'✅' if result == 'WIN' else '💀'} Result: {result}"
        )

    except Exception as e:
        return f"❌ Error checking trade: {str(e)}"