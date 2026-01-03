import os, sqlite3, requests, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

# Configuración de sistema de alto rendimiento
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

def get_db():
    """Conexión Blindada: Crea tablas al vuelo si faltan"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS leads 
                 (nombre TEXT, whatsapp TEXT, email TEXT, interes TEXT, fecha TIMESTAMP)''')
    conn.commit()
    return conn

def get_vision():
    """Consultoría Instantánea: Metas y Mercados"""
    res = {"oro": "N/D", "btc": "N/D", "plan": "Calculando ruta de cuatrillones..."}
    try:
        # Consulta de activos en un solo bloque para velocidad
        oro = yf.Ticker("GC=F").fast_info['last_price']
        btc = yf.Ticker("BTC-USD").fast_info['last_price']
        res.update({"oro": round(oro, 2), "btc": round(btc, 2)})
        res["plan"] = f"🔱 VMAX: ORO en ${res['oro']}. Foco en acumulación y captación VIP."
    except: pass
    return res

@app.route('/')
def dashboard():
    """Terminal de Control de 8,291 Millones"""
    v = get_vision()
    leads = []
    try:
        db = get_db()
        leads = db.execute('SELECT nombre, whatsapp, email, interes FROM leads ORDER BY fecha DESC LIMIT 15').fetchall()
        db.close()
    except: pass
    
    return render_template_string('''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:15px; font-size:14px;">
        <div style="border:2px solid #0f0; padding:10px; margin-bottom:15px; text-align:center;">
            <h1 style="margin:0;">🔱 VMAXPRO TERMINAL 🔱</h1>
            <h2 style="color:#fff;">META: $8,291,000,000</h2>
        </div>

        <div style="display:flex; justify-content:space-around; border:1px solid #0f0; padding:10px; margin-bottom:15px;">
            <span>💰 ORO: ${{v.oro}}</span>
            <span>💎 BTC: ${{v.btc}}</span>
        </div>

        <div style="border:1px solid #0f0; padding:10px; background:rgba(0,255,0,0.1); margin-bottom:15px;">
            <p style="margin:0;"><b>PLAN:</b> {{v.plan}}</p>
        </div>

        <div style="border:1px solid #0f0; padding:10px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <h3 style="margin:0;">👥 BÓVEDA DE LEADS</h3>
                <a href="/registro" target="_blank" style="background:#0f0; color:#000; padding:2px 8px; text-decoration:none; font-weight:bold;">REGISTRO VIP</a>
            </div>
            <table style="width:100%; color:#0f0; border-collapse:collapse; text-align:left; font-size:12px;">
                <tr style="border-bottom:1px solid #0f0;"><th>Socio</th><th>WhatsApp</th><th>Email</th><th>Interés</th></tr>
                {% for l in leads %}
                <tr style="border-bottom:0.5px solid #222;"><td>{{l[0]}}</td><td>{{l[1]}}</td><td>{{l[2]}}</td><td>{{l[3]}}</td></tr>
                {% endfor %}
            </table>
        </div>
    </body>
    ''', v=v, leads=leads)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Portal de Captura Profesional"""
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO leads VALUES (?,?,?,?,?)', 
                   (request.form['n'], request.form['w'], request.form['e'], request.form['i'], datetime.now()))
        db.commit()
        db.close()
        return "<body style='background:#000;color:#0f0;text-align:center;padding:50px;'><h1>🔱 REGISTRADO EN VMAXPRO.</h1><a href='/' style='color:#fff;'>Dashboard</a></body>"
    
    return '''
    <body style="background:#000; color:#0f0; font-family:sans-serif; text-align:center; padding:20px;">
        <h3>🔱 CLUB VIP VOLTAMAXPRO 🔱</h3>
        <form method="post" style="display:inline-block; text-align:left; border:1px solid #0f0; padding:20px; border-radius:8px;">
            NOMBRE:<br><input name="n" style="width:220px;margin-bottom:10px;" required><br>
            WHATSAPP:<br><input name="w" style="width:220px;margin-bottom:10px;" required><br>
            EMAIL:<br><input type="email" name="e" style="width:220px;margin-bottom:10px;" required><br>
            INTERÉS (OPCIONAL):<br><textarea name="i" style="width:220px;height:40px;"></textarea><br><br>
            <button type="submit" style="background:#0f0; color:#000; width:100%; padding:10px; font-weight:bold; border:none; cursor:pointer;">SOLICITAR ACCESO</button>
        </form>
    </body>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
