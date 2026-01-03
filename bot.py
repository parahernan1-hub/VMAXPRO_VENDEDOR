import os, sqlite3, requests, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

# CONFIGURACIÓN DE TU IMPERIO (Pon esto en Render > Environment)
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS leads (nombre TEXT, whatsapp TEXT, email TEXT, interes TEXT, fecha TIMESTAMP)')
    conn.commit()
    return conn

def vision_millonaria():
    v = {"oro": 0, "btc": 0, "prod_top": "Sin Conexión", "consejo": "Conecta Shopify para analizar productos."}
    try:
        v["oro"] = round(yf.Ticker("GC=F").fast_info['last_price'], 2)
        v["btc"] = round(yf.Ticker("BTC-USD").fast_info['last_price'], 2)
        
        if SHOPIFY_TOKEN and SHOP_URL:
            # Conexión real a tus productos
            h = {"X-Shopify-Access-Token": SHOPIFY_TOKEN}
            r = requests.get(f"https://{SHOP_URL}/admin/api/2023-10/products.json?limit=1", headers=h)
            if r.status_code == 200:
                p = r.json()['products'][0]
                v["prod_top"] = p['title']
                v["consejo"] = f"🔱 VMAX: Tu producto '{p['title']}' tiene potencial. ¡Sube el presupuesto en anuncios!"
    except: pass
    return v

@app.route('/')
def dashboard():
    v = vision_millonaria()
    db = get_db()
    leads = db.execute('SELECT * FROM leads ORDER BY fecha DESC LIMIT 10').fetchall()
    db.close()
    
    return render_template_string('''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:15px;">
        <div style="border:2px solid #0f0; padding:10px; text-align:center; margin-bottom:20px;">
            <h1 style="margin:0;">🔱 VMAXPRO TERMINAL 🔱</h1>
            <h3 style="color:#fff;">META: $8,291,000,000</h3>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:20px;">
            <div style="border:1px solid #0f0; padding:10px;">
                <p>💰 ORO: ${{v.oro}}</p>
                <p>💎 BTC: ${{v.btc}}</p>
            </div>
            <div style="border:1px solid #0f0; padding:10px;">
                <p>🏬 TOP PRODUCTO: {{v.prod_top}}</p>
                <p style="color:#ff0;">{{v.consejo}}</p>
            </div>
        </div>

        <div style="border:1px solid #0f0; padding:10px;">
            <h3>👥 BÓVEDA DE LEADS (SOCIOS VIP)</h3>
            <table style="width:100%; color:#0f0; border-collapse:collapse; font-size:12px;">
                <tr style="border-bottom:1px solid #0f0;"><th>Nombre</th><th>WhatsApp</th><th>Email</th></tr>
                {% for l in leads %}
                <tr><td>{{l[0]}}</td><td>{{l[1]}}</td><td>{{l[2]}}</td></tr>
                {% endfor %}
            </table>
            <br>
            <a href="/registro" style="background:#0f0; color:#000; padding:5px; text-decoration:none; font-weight:bold;">REGISTRAR NUEVO SOCIO</a>
        </div>
    </body>
    ''', v=v, leads=leads)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO leads VALUES (?,?,?,?,?)', (request.form['n'], request.form['w'], request.form['e'], '', datetime.now()))
        db.commit(); db.close()
        return "<h1>🔱 SOCIO REGISTRADO.</h1><a href='/'>Volver</a>"
    return '<body style="background:#000;color:#0f0;text-align:center;"><form method="post">Nombre:<br><input name="n"><br>WhatsApp:<br><input name="w"><br>Email:<br><input name="e"><br><br><button type="submit">UNIRSE AL CLUB</button></form></body>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
