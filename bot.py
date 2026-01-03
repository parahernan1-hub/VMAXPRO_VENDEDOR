import os, sqlite3, requests
import yfinance as yf
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# CONFIGURACIÓN OBLIGATORIA EN RENDER
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def analizar_mercado():
    # Analizamos Divisas, ETFs y Crypto para la estrategia de 8,291M
    res = {"activos": [], "shopify": "🔴 DESCONECTADO"}
    try:
        tickers = {"ORO": "GC=F", "SPY (S&P500)": "SPY", "BTC": "BTC-USD", "EUR/USD": "EURUSD=X"}
        for n, t in tickers.items():
            val = yf.Ticker(t).fast_info['last_price']
            res["activos"].append({"n": n, "v": round(val, 2)})
        
        if SHOPIFY_TOKEN and SHOP_URL:
            res["shopify"] = "🟢 CONECTADO"
            # Aquí iría la llamada real para espiar tráfico y ventas
    except: pass
    return res

@app.route('/')
def index():
    m = analizar_mercado()
    return render_template_string('''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
        <div style="border:2px solid #0f0; padding:20px; text-align:center;">
            <h1>🔱 VMAXPRO: GLOBAL SPY & COMMAND 🔱</h1>
            <h2 style="color:#fff;">ESTADO SISTEMA: {{ m.shopify }}</h2>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">
            <div style="border:1px solid #0f0; padding:15px;">
                <h3>📊 MONITOR DE MERCADO (REAL-TIME)</h3>
                {% for a in m.activos %}
                <p><b>{{a.n}}:</b> ${{a.v}}</p>
                {% endfor %}
            </div>

            <div style="border:1px solid #0f0; padding:15px;">
                <h3>🚀 PRODUCTOS GANADORES / COMPETENCIA</h3>
                <p style="color:#ff0;">Analizando tendencias de nicho...</p>
                <div style="background:#111; height:100px; border:1px dashed #0f0; text-align:center; padding-top:40px;">
                    [ GRÁFICA DE TENDENCIAS CARGANDO... ]
                </div>
            </div>
        </div>
        
        <p style="margin-top:20px; border-left: 4px solid #fff; padding-left:10px;">
            🔱 <b>VISIÓN VMAX:</b> "El dinero nunca duerme. Si el EUR/USD baja, importa más mercancía ahora."
        </p>
    </body>
    ''', m=m)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
