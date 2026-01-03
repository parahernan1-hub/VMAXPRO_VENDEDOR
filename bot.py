import os, sqlite3, requests, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

# --- CONFIGURACIÓN DE SEGURIDAD (Render Environment) ---
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN') # Aquí irá tu shpss_...
SHOP_URL = os.environ.get('SHOP_URL')       # Ejemplo: tu-tienda.myshopify.com

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS leads (nombre TEXT, whatsapp TEXT, interes TEXT, fecha TIMESTAMP)')
    logger.info("✅ DB VMAX LISTA")

# --- LÓGICA DE INTELIGENCIA FINANCIERA Y PRODUCTOS ---
def obtener_vision_vmax():
    try:
        # Analiza Oro y Litio (Mercado de energía y refugio)
        oro = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        
        # Conexión a Shopify para ver tus productos
        headers = {"X-Shopify-Access-Token": SHOPIFY_TOKEN}
        shop_data = "Sin conexión"
        if SHOPIFY_TOKEN and SHOP_URL:
            url = f"https://{SHOP_URL}/admin/api/2023-10/products.json?limit=1"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                prods = r.json().get('products', [])
                shop_data = f"Conectado: {len(prods)} productos detectados."
            else:
                shop_data = "Error de conexión (Revisa el Token)"

        return {
            "oro": round(oro, 2),
            "shop": shop_data,
            "oportunidad": "🔱 VMAX VISION: Alta demanda en accesorios de Litio. Revisa precios en tu Shopify."
        }
    except Exception as e:
        return {"oro": "N/D", "shop": str(e), "oportunidad": "Analizando..."}

# --- DASHBOARD PROFESIONAL ---
@app.route('/')
def dashboard():
    vision = obtener_vision_vmax()
    with sqlite3.connect(DB_PATH) as conn:
        leads = conn.execute('SELECT * FROM leads ORDER BY fecha DESC LIMIT 5').fetchall()
    
    html = f'''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h1 style="text-shadow: 0 0 10px #0f0;">🔱 VOLTAMAXPRO VISIONARY SYSTEM 🔱</h1>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
            <div style="border:1px solid #0f0; padding:15px;">
                <h3>📈 MERCADO GLOBAL</h3>
                <p>ORO: ${vision['oro']} USD</p>
                <p style="color:#ff0;">{vision['oportunidad']}</p>
            </div>
            <div style="border:1px solid #0f0; padding:15px;">
                <h3>🏬 MI SHOPIFY</h3>
                <p>Estado: {vision['shop']}</p>
                <p>Arbitraje: Buscando mejores precios...</p>
            </div>
        </div>
        <div style="margin-top:20px; border:1px solid #0f0; padding:15px;">
            <h3>👥 ÚLTIMOS CLIENTES CAPTADOS</h3>
            <table border="1" style="width:100%; color:#0f0; border-collapse:collapse;">
                <tr><th>Nombre</th><th>WhatsApp</th><th>Interés</th></tr>
                {''.join(f"<tr><td>{l[0]}</td><td>{l[1]}</td><td>{l[2]}</td></tr>" for l in leads)}
            </table>
            <br>
            <a href="/registro" style="color:#000; background:#0f0; padding:5px;">LINK PARA TUS REDES</a>
        </div>
    </body>
    '''
    return render_template_string(html)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('INSERT INTO leads VALUES (?, ?, ?, ?)', 
                         (request.form['n'], request.form['w'], request.form['i'], datetime.now()))
        return "<h1>🔱 Registrado en VMAX.</h1><a href='/registro'>Volver</a>"
    return '''
    <body style="background:#000; color:#0f0; text-align:center; padding:50px;">
        <h2>🔱 CLUB VIP VOLTAMAXPRO 🔱</h2>
        <form method="post">
            <input name="n" placeholder="Nombre" required><br><br>
            <input name="w" placeholder="WhatsApp" required><br><br>
            <select name="i"><option value="Baterias">Baterías</option><option value="Inversion">Inversión</option></select><br><br>
            <button type="submit">UNIRME AL CLUB</button>
        </form>
    </body>
    '''

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=10000)
