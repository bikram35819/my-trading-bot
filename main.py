import time
import requests
import threading
from flask import Flask

app = Flask(__name__)

# 🔑 Tomar real Groq key ekhane string-e thakbe
GROQ_API_KEY = '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'.strip()

virtual_balance_usdt = 10000.0
virtual_btc_holding = 0.0

def ask_ai_swarm_agents(price_data, news_title):
    prompt = f"Asset: BTC/USDT. Price: ${price_data}. News: {news_title}. Debaters: Bull, Bear, Judge. Last line must be exactly 'SIGNAL: BUY' or 'SIGNAL: HOLD'."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.4}
    try:
        res = requests.post(url, headers=headers, json=data).json()
        ai_reply = res['choices'][0]['message']['content']
        if "SIGNAL: BUY" in ai_reply.upper(): return "BUY"
        return "HOLD"
    except:
        return "HOLD"

def run_trading_bot():
    global virtual_balance_usdt, virtual_btc_holding
    while True:
        try:
            ticker_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
            current_price = float(ticker_res['price'])
            mock_news = "Bitcoin institutional adoption hits record high as major banks add BTC to balance sheets."
            
            decision = ask_ai_swarm_agents(current_price, mock_news)
            
            if decision == "BUY" and virtual_balance_usdt >= (0.1 * current_price):
                virtual_balance_usdt -= (0.1 * current_price)
                virtual_btc_holding += 0.1
                print(f"[CLOUD] Virtual BUY Executed! Wallet: ${virtual_balance_usdt:.2f}")
            
            time.sleep(60)
        except Exception as e:
            time.sleep(10)

@app.route('/')
def home():
    return f"<h3>Bot Operational Status: ACTIVE 24/7</h3><p>Wallet Balance: ${virtual_balance_usdt:.2f} USDT</p><p>BTC Holdings: {virtual_btc_holding} BTC</p>"

if __name__ == "__main__":
    threading.Thread(target=run_trading_bot).start()
    app.run(host="0.0.0.0", port=8080)
  
