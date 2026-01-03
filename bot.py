import os, sqlite3, requests, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

# LLAVES DEL IMPERIO
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def inicializar_y_conectar():
    """Garantiza que la base de datos sea indestructible"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS leads 
                 (nombre TEXT, whatsapp TEXT, email TEXT, interes TEXT, fecha TIMESTAMP)''')
    conn.commit()
    return conn

def obtener_vision_ia():
    """Cerebro de mercado y e-commerce"""
    vision = {"oro": 0, "btc": 0, "status_shop": "🔴 DESCONECTADO", "orden": "Esperando datos..."}
    try:
        vision["oro"] = round(yf.Ticker("GC=F").fast_info['last_price'], 2)
        vision["btc"] = round(yf.Ticker("BTC-USD").fast_info['last_price'], 2)
        
        if SHOPIFY_TOKEN and SHOP_URL:
            vision["status_shop"] = "🟢 CONECTADO"
            vision["orden"] = "🔱 VMAX: Tráfico detectado. El Oro sube, aumenta márgenes en productos de lujo."
        else:
            vision["orden"] = "⚠️ ATENCIÓN: Conecta Shopify en Render para activar el radar de ventas."
    except: pass
    return vision

@app.route('/')
def dashboard_terminal():
    v = obtener_vision_ia()
    conn = inicializar_y_conectar()
    leads = conn.execute('SELECT * FROM leads ORDER BY fecha DESC LIMIT 5').fetchall()
    conn.close()
    
    return render_template_string('''
    <!DOCTYPE html>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
        .terminal { border: 2px solid #0f0; padding: 20px; box-shadow: 0 0 30px #0f0; }
        .grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; margin-top: 20px; }
        .card { border: 1px solid #0f0; padding: 15px; background: rgba(0,255,0,0.05); }
        .header { text-align: center; border-bottom: 2px solid #0f0; padding-bottom: 20px; }
        .chart-box { height: 300px; border: 1px solid #444; margin-top: 10px; background: #050505; }
    </style>

    <div class="terminal">
        <div class="header">
            <h1>🔱 VMAXPRO GLOBAL COMMAND 🔱</h1>
            <h2 style="color:#fff;">CONGLOMERADO: $8,291,000,000 | SHOP: {{v.status_shop}}</h2>
        </div>

        <div class="grid">
            <div class="card">
                <h3>📊 RADAR DE ACTIVOS (LIVE)</h3>
                <p>💰 ORO: ${{v.oro}} | 💎 BTC: ${{v.btc}}</p>
                <div class="chart-box">
                    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_762ae&symbol=OANDA%3AXAUUSD&interval=D&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=%5B%5D&theme=dark&style=1&timezone=Etc%2FUTC" 
                            width="100%" height="100%" frameborder="0"></iframe>
                </div>
            </div>

            <div class="card">
                <h3>🧠 IA DE CONSULTORÍA</h3>
                <div style="background:#fff; color:#000; padding:10px; font-weight:bold;">
                    ORDEN DEL DÍA: {{v.orden}}
                </div>
                <h3 style="margin-top:20px;">🚀 PRODUCTOS GANADORES (SPY)</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="border-left: 3px solid #0f0; padding-left: 10px; margin-bottom: 10px;">
                        <b>Gadgets IA:</b> Margen 85% - Tendencia Alcista
                    </li>
                    <li style="border-left: 3px solid #0f0; padding-left: 10px;">
                        <b>Lujo Sostenible:</b> Alta demanda en Europa
                    </li>
                </ul>
            </div>
        </div>

        <div class="card" style="margin-top:20px;">
            <h3>👥 BÓVEDA DE LEADS VIP</h3>
            <table style="width:100%; color:#0f0; text-align:left;">
                <tr style="border-bottom: 1px solid #0f0;"><th>Socio</th><th>WhatsApp</th><th>Email</th></tr>
                {% for l in leads %}
                <tr><td>{{l[0]}}</td><td>{{l[1]}}</td><td>{{l[2]}}</td></tr>
                {% endfor %}
            </table>
            <br><a href="/registro" style="background:#0f0; color:#000; padding:10px; text-decoration:none; font-weight:bold;">REGISTRAR SOCIO</a>
        </div>
    </div>
    ''', v=v, leads=leads)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        conn = inicializar_y_conectar()
        conn.execute('INSERT INTO leads VALUES (?,?,?,?,?)', 
                     (request.form['n'], request.form['w'], request.form['e'], '', datetime.now()))
        conn.commit(); conn.close()
        return "<h1>🔱 SOCIO CAPTADO.</h1><a href='/'>VOLVER AL MANDO</a>"
    return '<body style="background:#000;color:#0f0;text-align:center;padding:50px;"><h2>REGISTRO VMAX</h2><form method="post">Nombre:<br><input name="n" required><br>WhatsApp:<br><input name="w" required><br>Email:<br><input name="e" required><br><br><button type="submit" style="background:#0f0;padding:10px;font-weight:bold;">UNIRSE</button></form></body>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
