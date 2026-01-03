import os, sqlite3, requests, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        # Añadimos la columna 'email' a la base de datos
        conn.execute('''CREATE TABLE IF NOT EXISTS leads 
                     (nombre TEXT, whatsapp TEXT, email TEXT, interes TEXT, fecha TIMESTAMP)''')
    logger.info("✅ DB VMAX LISTA CON CORREO ELECTRÓNICO")

def obtener_vision_vmax():
    vision = {"oro": "N/D", "shop": "Cargando...", "oportunidad": "Analizando mercado..."}
    try:
        oro = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        vision["oro"] = round(oro, 2)
        if SHOPIFY_TOKEN and SHOP_URL:
            vision["shop"] = "Conectado ✅"
            vision["oportunidad"] = "🔱 VMAX: Sistema de arbitraje activo. Analizando productos ganadores."
    except: pass
    return vision

@app.route('/')
def dashboard():
    vision = obtener_vision_vmax()
    with sqlite3.connect(DB_PATH) as conn:
        leads = conn.execute('SELECT nombre, whatsapp, email, interes FROM leads ORDER BY fecha DESC LIMIT 10').fetchall()
    
    html = f'''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
        <h1 style="text-shadow: 0 0 10px #0f0; text-align:center;">🔱 VOLTAMAXPRO SYSTEM 🔱</h1>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; margin-bottom:20px;">
            <div style="border:1px solid #0f0; padding:10px; border-radius:10px;">
                <h3>📈 FINANZAS GLOBALES</h3>
                <p>ORO: ${vision['oro']} USD</p>
                <p style="color:#ff0;">{vision['oportunidad']}</p>
            </div>
            <div style="border:1px solid #0f0; padding:10px; border-radius:10px;">
                <h3>🏬 SHOPIFY E-COMMERCE</h3>
                <p>ESTADO: {vision['shop']}</p>
            </div>
        </div>
        <div style="border:1px solid #0f0; padding:10px; border-radius:10px;">
            <h3>👥 BASE DE DATOS CLIENTES VIP</h3>
            <table border="1" style="width:100%; color:#0f0; border-collapse:collapse; text-align:left;">
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
        return "<body style='background:#000;color:#0f0;text-align:center;padding-top:100px;font-family:sans-serif;'><h1>🔱 REGISTRO EXITOSO 🔱</h1><p>Bienvenido al Círculo VoltamaxPro.</p><a href='/registro' style='color:#fff;'>Volver</a></body>"
    
    return '''
    <body style="background:#000; color:#0f0; font-family:sans-serif; text-align:center; padding:30px;">
        <h2 style="letter-spacing:2px;">🔱 ÚNETE A VOLTAMAXPRO 🔱</h2>
        <p>Introduce tus datos para acceder a oportunidades exclusivas.</p><br>
        <form method="post" style="display:inline-block; text-align:left; border:1px solid #0f0; padding:30px; border-radius:15px; width:90%; max-width:350px;">
            <label>NOMBRE COMPLETO:</label><br>
            <input name="n" style="width:100%; margin-bottom:15px; padding:10px; border:1px solid #0f0; background:#111; color:#0f0;" required><br>
            
            <label>WHATSAPP (con código):</label><br>
            <input name="w" placeholder="+34..." style="width:100%; margin-bottom:15px; padding:10px; border:1px solid #0f0; background:#111; color:#0f0;" required><br>
            
            <label>CORREO ELECTRÓNICO:</label><br>
            <input type="email" name="e" placeholder="ejemplo@correo.com" style="width:100%; margin-bottom:15px; padding:10px; border:1px solid #0f0; background:#111; color:#0f0;" required><br>
            
            <label>¿EN QUÉ ESTÁS INTERESADO? (Opcional):</label><br>
            <textarea name="i" style="width:100%; height:80px; margin-bottom:20px; border:1px solid #0f0; background:#111; color:#0f0;"></textarea><br>
            
            <button type="submit" style="background:#0f0; color:#000; width:100%; padding:15px; font-weight:bold; border:none; cursor:pointer; text-transform:uppercase;">SOLICITAR ACCESO VIP</button>
        </form>
    </body>
    '''

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
