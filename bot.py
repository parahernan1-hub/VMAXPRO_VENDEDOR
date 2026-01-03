import os, sqlite3, requests, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

# Configuración de Logs para que veas todo en Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

# --- CONFIGURACIÓN DE SEGURIDAD (Render Environment) ---
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def init_db():
    """Crea la base de datos y las tablas si no existen para evitar errores 500"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS leads 
                         (nombre TEXT, whatsapp TEXT, interes TEXT, fecha TIMESTAMP)''')
            conn.commit()
        logger.info("✅ Base de Datos VMAX inicializada correctamente.")
    except Exception as e:
        logger.error(f"❌ Error crítico en DB: {e}")

# --- LÓGICA DE INTELIGENCIA DE MERCADO ---
def obtener_vision_vmax():
    try:
        # Analiza Oro (Refugio financiero)
        oro = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        
        # Conexión a Shopify
        headers = {"X-Shopify-Access-Token": SHOPIFY_TOKEN}
        shop_data = "No configurado"
        if SHOPIFY_TOKEN and SHOP_URL:
            url = f"https://{SHOP_URL}/admin/api/2023-10/products.json?limit=1"
            r = requests.get(url, headers=headers, timeout=5)
            shop_data = "Conectado" if r.status_code == 200 else f"Error {r.status_code}"

        return {
            "oro": round(oro, 2),
            "shop": shop_data,
            "oportunidad": "🔱 VMAX: El Litio es el nuevo oro. Revisa stock de baterías."
        }
    except:
        return {"oro": "N/D", "shop": "Cargando...", "oportunidad": "Analizando mercado..."}

# --- DASHBOARD DE CONTROL (La pantalla verde) ---
@app.route('/')
def dashboard():
    vision = obtener_vision_vmax()
    leads = []
    try:
        with sqlite3.connect(DB_PATH) as conn:
            leads = conn.execute('SELECT nombre, whatsapp, interes FROM leads ORDER BY fecha DESC LIMIT 5').fetchall()
    except:
        init_db() # Si falla por falta de tabla, la crea al momento

    html = f'''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
        <h1 style="text-shadow: 0 0 10px #0f0;">🔱 VOLTAMAXPRO - VISIONARY SYSTEM 🔱</h1>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
            <div style="border:2px solid #0f0; padding:15px; border-radius:10px;">
                <h3>📈 MERCADO GLOBAL</h3>
                <p>ORO: ${vision['oro']} USD</p>
                <p style="color:#ff0;">{vision['oportunidad']}</p>
            </div>
            <div style="border:2px solid #0f0; padding:15px; border-radius:10px;">
                <h3>🏬 ESTADO SHOPIFY</h3>
                <p>Conexión: {vision['shop']}</p>
                <p>Arbitraje: Modo activo.</p>
            </div>
        </div>
        <div style="margin-top:20px; border:2px solid #0f0; padding:15px; border-radius:10px;">
            <h3>👥 ÚLTIMOS CLIENTES CAPTADOS (CLUB VIP)</h3>
            <table style="width:100%; color:#0f0; border-collapse:collapse; text-align:left;">
                <tr style="border-bottom: 1px solid #0f0;"><th>Nombre</th><th>WhatsApp</th><th>Interés</th></tr>
                {''.join(f"<tr><td>{l[0]}</td><td>{l[1]}</td><td>{l[2]}</td></tr>" for l in leads)}
            </table>
            <br>
            <a href="/registro" style="color:#000; background:#0f0; padding:10px; text-decoration:none; font-weight:bold;">OBTENER LINK PARA REDES</a>
        </div>
    </body>
    '''
    return render_template_string(html)

# --- PORTAL DE CAPTACIÓN (Sin Meta, sin límites) ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute('INSERT INTO leads VALUES (?, ?, ?, ?)', 
                             (request.form['n'], request.form['w'], request.form['i'], datetime.now()))
                conn.commit()
            return "<h1>🔱 ¡Bienvenido al Club VIP de VoltamaxPro! Pronto nos pondremos en contacto.</h1><a href='/'>Volver al Dashboard</a>"
        except:
            return "Error al registrar. Inténtalo de nuevo."
            
    return '''
    <body style="background:#000; color:#0f0; font-family:sans-serif; text-align:center; padding:50px;">
        <h2>🔱 ÚNETE AL CLUB VIP VOLTAMAXPRO 🔱</h2>
        <p>Accede a productos exclusivos y análisis de inversión antes que nadie.</p><br>
        <form method="post" style="display:inline-block; text-align:left; border:1px solid #0f0; padding:20px;">
            Nombre:<br><input name="n" style="width:250px" required><br><br>
            WhatsApp:<br><input name="w" style="width:250px" required><br><br>
            Interés:<br>
            <select name="i" style="width:258px">
                <option value="Baterias">Baterías y Energía</option>
                <option value="Inversion">Inversión y Finanzas</option>
                <option value="Bienes Raices">Bienes Raíces</option>
            </select><br><br>
            <button type="submit" style="background:#0f0; color:#000; width:100%; padding:10px; cursor:pointer;">REGISTRARME</button>
        </form>
    </body>
    '''

if __name__ == "__main__":
    init_db() # Asegura que la tabla exista al arrancar
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
