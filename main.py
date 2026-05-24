import time
import requests
import threading
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# =================================================================
# 🔑 SECURITY LOGIC: TOMAR GROQ API KEY-TA EKHANE BOSHRE DAO
# =================================================================
GROQ_API_KEY = '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'.strip()
# =================================================================

# Global Variables for Realtime Tracking Stream
virtual_balance_usdt = 10000.0
virtual_btc_holding = 0.0
action_logs = []  # Live action log list storage

def log_action(message):
    global action_logs
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action_logs.insert(0, {"time": timestamp, "msg": message})
    # List size fixed to 20 for memory optimization
    if len(action_logs) > 20:
        action_logs.pop()

def ask_ai_swarm_agents(price_data, news_title):
    log_action("🧠 AI Swarm Debate Triggered: 3 Agents analyzing market context...")
    
    prompt = f"""
    Asset: BTC/USDT. Current Price: ${price_data}. News: "{news_title}".
    Personas: Bullish Analyst, Bearish Skeptic, Judge.
    Provide a quick consensus. CRITICAL: Your last line must be exactly either 'SIGNAL: BUY' or 'SIGNAL: HOLD'.
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.4}
    
    try:
        res = requests.post(url, headers=headers, json=data).json()
        ai_reply = res['choices'][0]['message']['content']
        
        # Split lines to inspect agent summary
        for line in ai_reply.split('\n'):
            if line.strip():
                log_action(f"💬 {line.strip()}")
                
        if "SIGNAL: BUY" in ai_reply.upper(): 
            return "BUY"
        return "HOLD"
    except Exception as e:
        log_action(f"🚨 Groq API Error Network Connection Refused: {e}")
        return "HOLD"

def run_trading_bot():
    global virtual_balance_usdt, virtual_btc_holding
    log_action("🚀 Automated Crypto Engine Background Active Non-Stop.")
    
    while True:
        try:
            # Fetch Live Data from Binance Public Endpoint
            ticker_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
            current_price = float(ticker_res['price'])
            
            mock_news = "Bitcoin institutional accumulation pattern accelerates as network whale addresses spike."
            log_action(f"📈 Price Pulse Check: Live BTC Price is ${current_price}")
            
            decision = ask_ai_swarm_agents(current_price, mock_news)
            
            if decision == "BUY":
                trade_cost = 0.1 * current_price
                if virtual_balance_usdt >= trade_cost:
                    virtual_balance_usdt -= trade_cost
                    virtual_btc_holding += 0.1
                    log_action(f"🟢 [TRADE SUCCESS] AI Order BUY Executed! Bought 0.1 BTC at ${current_price}")
                else:
                    log_action("⚠️ [RISK BLOCK] Order BUY skipped: Insufficient virtual USDT balance.")
            else:
                log_action("⚖️ AI Consensus: HOLD position. Scanning market stability indices.")
                
            # ⏰ Token Limit Saver Block: 5 Minutes Interval (300 seconds)
            time.sleep(300)
            
        except Exception as e:
            log_action(f"⚠️ System Matrix Glitch: {e}")
            time.sleep(15)

# HTML Dashboard Template with Premium Dark Mode & TradingView Widget Integration
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LoreSphere Prime | AI Swarm Trading Terminal</title>
    <script src="https://cdn.jsdelivr.net/npm/tailwind-css-cdn@1.3.1/dist/tailwind.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased min-h-screen">

    <header class="border-b border-gray-800 bg-gray-900 px-6 py-4 flex justify-between items-center shadow-lg">
        <div class="flex items-center space-x-3">
            <div class="h-4 w-4 rounded-full bg-green-500 animate-pulse"></div>
            <h1 class="text-xl font-bold tracking-wider text-green-400">LORESPHERE PRIME AI TERMINAL</h1>
        </div>
        <div class="text-sm bg-gray-800 px-3 py-1 rounded-full text-gray-400 border border-gray-700">
            System Mode: <span class="text-green-400 font-semibold text-xs">PAPER TRADING (100% FREE)</span>
        </div>
    </header>

    <main class="p-6 max-w-7xl mx-auto space-y-6">
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-md flex flex-col justify-between">
                <span class="text-xs uppercase tracking-widest text-gray-500 font-bold">Virtual Wallet Cash</span>
                <span class="text-3xl font-extrabold text-green-400 mt-2">${{ "%.2f"|format(balance) }} <span class="text-sm font-medium text-gray-400">USDT</span></span>
            </div>
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-md flex flex-col justify-between">
                <span class="text-xs uppercase tracking-widest text-gray-500 font-bold">BTC Crypto Holdings</span>
                <span class="text-3xl font-extrabold text-blue-400 mt-2">{{ btc }} <span class="text-sm font-medium text-gray-400">BTC</span></span>
            </div>
            <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-md flex flex-col justify-between">
                <span class="text-xs uppercase tracking-widest text-gray-500 font-bold">Bot Status</span>
                <span class="text-lg font-bold text-gray-200 mt-2 flex items-center space-x-2">
                    <span class="h-2 w-2 rounded-full bg-green-400 inline-block"></span>
                    <span>ONLINE & ACTIVE 24/7</span>
                </span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div class="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-4 shadow-md h-96">
                <h3 class="text-sm font-semibold tracking-wider text-gray-400 mb-3 uppercase">Live TradingView Candle Chart</h3>
                <div class="w-full h-full pb-8">
                    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE%3ABTCUSDT&interval=5&hidesidetoolbar=1&symboledit=0&saveimage=1&toolbarbg=f1f3f6&studies=%5B%5D&theme=dark&style=1&timezone=Etc%2FUTC&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=%5B%5D&disabled_features=%5B%5D&locale=en" class="w-full h-full border-0 rounded-lg"></iframe>
                </div>
            </div>

            <div class="bg-gray-900 border border-gray-800 rounded-xl p-4 shadow-md flex flex-col h-96">
                <h3 class="text-sm font-semibold tracking-wider text-gray-400 mb-3 uppercase">Live Action Stream</h3>
                <div class="flex-1 overflow-y-auto space-y-2 pr-1 font-mono text-xs">
                    {% for log in logs %}
                    <div class="p-2 rounded bg-gray-950 border border-gray-800 leading-relaxed">
                        <span class="text-gray-600 font-sans block text-[10px]">{{ log.time }}</span>
                        <span class="text-gray-300">{{ log.msg }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>

        </div>

    </main>

    <footer class="text-center text-xs text-gray-600 py-8 border-t border-gray-900 mt-12 font-mono">
        LoreSphere Prime Trading System Framework v2.0 • Data refreshed automatically via web browser client.
    </footer>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(
        DASHBOARD_HTML, 
        balance=virtual_balance_usdt, 
        btc=virtual_btc_holding, 
        logs=action_logs
    )

if __name__ == "__main__":
    threading.Thread(target=run_trading_bot).start()
    app.run(host="0.0.0.0", port=8080)
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
  
