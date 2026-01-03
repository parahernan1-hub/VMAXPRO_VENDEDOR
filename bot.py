import os, sqlite3, requests, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

# Variables de entorno seguras
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS leads 
                     (nombre TEXT, whatsapp TEXT, email TEXT, interes TEXT, fecha TIMESTAMP)''')
    logger.info("✅ INFRAESTRUCTURA VMAX LISTA")

def obtener_vision_vmax():
    # Meta inicial: 8,291 Millones
    vision = {"oro": 0, "btc": 0, "eurusd": 0, "shop": "Desconectado", "plan": ""}
    try:
        # Rastreadores de Activos Globales
        oro = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
        eurusd = yf.Ticker("EURUSD=X").history(period="1d")['Close'].iloc[-1]
        
        vision.update({"oro": round(oro, 2), "btc": round(btc, 2), "eurusd": round(eurusd, 4)})

        # Inteligencia de Shopify
        if SHOPIFY_TOKEN and SHOP_URL:
            vision["shop"] = "Sincronizado ✅"
            
        # El Consultor Visionario: Plan del día para los 8,291M
        if btc > 60000:
            vision["plan"] = "🔱 VMAX: El mercado crypto está fuerte. Reinvierte beneficios de Shopify en BTC. Busca proveedores en Europa (EUR bajo)."
        else:
            vision["plan"] = "🔱 VMAX: Oro al alza. Protege capital. Sube precios en Shopify un 3% para cubrir inflación."
            
    except: pass
    return vision

@app.route('/')
def dashboard():
    v = obtener_vision_vmax()
    with sqlite3.connect(DB_PATH) as conn:
        leads = conn.execute('SELECT nombre, whatsapp, email, interes FROM leads ORDER BY fecha DESC LIMIT 10').fetchall()
    
    html = f'''
    <body style="background:#000; color:#0f0; font-family:'Courier New', monospace; padding:20px;">
        <h1 style="text-shadow: 0 0 15px #0f0; text-align:center;">🔱 VMAXPRO GLOBAL CONSULTANCY 🔱</h1>
        
        <div style="border:2px solid #0f0; padding:10px; margin-bottom:20px; text-align:center; background:rgba(0,255,0,0.1);">
            <h2 style="margin:0;">🎯 META ACTUAL: $8,291,000,000</h2>
            <p>Estatus: Analizando rutas de arbitraje y activos de refugio...</p>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin-bottom:20px;">
            <div style="border:1px solid #0f0; padding:15px;">
                <h3>💰 FINANZAS</h3>
                <p>ORO: ${v['oro']}</p>
                <p>BITCOIN: ${v['btc']}</p>
                <p>EUR/USD: {v['eurusd']}</p>
            </div>
            <div style="border:1px solid #0f0; padding:15px;">
                <h3>🏪 VMAX E-COMMERCE</h3>
                <p>Shopify: {v['shop']}</p>
                <p>Arbitraje: Rastreando productos ganadores...</p>
            </div>
            <div style="border:1px solid #0f0; padding:15px; color:#fff; background:#003300;">
                <h3>🧠 PLAN DE ACCIÓN HOY</h3>
                <p>{v['plan']}</p>
            </div>
        </div>

        <div style="border:1px solid #0f0; padding:15px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3>👥 SOCIOS CLUB VIP DETECTADOS</h3>
                <a href="/registro" target="_blank" style="background:#0f0; color:#000; padding:5px 10px; text-decoration:none; font-weight:bold;">ABRIR PORTAL REGISTRO</a>
            </div>
            <table border="1" style="width:100%; color:#0f0; border-collapse:collapse; margin-top:10px;">
                <tr><th>Nombre</th><th>WhatsApp</th><th>Email</th><th>Interés</th></tr>
                {''.join(f"<tr><td>{l[0]}</td><td>{l[1]}</td><td>{l[2]}</td><td>{l[3]}</td></tr>" for l in leads)}
            </table>
        </div>
    </body>
    '''
    return render_template_string(html)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('INSERT INTO leads VALUES (?, ?, ?, ?, ?)', 
                         (request.form['n'], request.form['w'], request.form['e'], request.form['i'], datetime.now()))
            conn.commit()
        return "<body style='background:#000;color:#0f0;text-align:center;padding-top:100px;'><h1>🔱 ACCESO SOLICITADO.</h1><p>VMAXPRO VISIONARY te contactará.</p></body>"
    return '''
    <body style="background:#000; color:#0f0; font-family:sans-serif; text-align:center; padding:30px;">
        <h2>🔱 VOLTAMAXPRO ELITE 🔱</h2>
        <form method="post" style="display:inline-block; border:1px solid #0f0; padding:30px; text-align:left;">
            Nombre:<br><input name="n" style="width:100%;" required><br><br>
            WhatsApp:<br><input name="w" style="width:100%;" required><br><br>
            Email:<br><input type="email" name="e" style="width:100%;" required><br><br>
            ¿En qué podemos ayudarte?<br><textarea name="i" style="width:100%; height:50px;"></textarea><br><br>
            <button type="submit" style="background:#0f0; width:100%; padding:10px; font-weight:bold; cursor:pointer;">SOLICITAR ACCESO VIP</button>
        </form>
    </body>
    '''

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
