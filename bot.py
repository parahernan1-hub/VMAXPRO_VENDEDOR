import os, sqlite3, threading, logging
import yfinance as yf
from flask import Flask, render_template_string, request
from datetime import datetime

# Configuración de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
DB_PATH = "vmax_matrix.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS leads (nombre TEXT, whatsapp TEXT, interes TEXT, fecha TIMESTAMP)')
        conn.execute('CREATE TABLE IF NOT EXISTS tendencias (producto TEXT, score REAL, fecha TIMESTAMP)')
    logger.info("✅ Base de Datos VMAX - Modo Visionario Lista.")

# --- LÓGICA DE INTELIGENCIA (EL BUSCADOR DE MILLONES) ---
def buscar_oportunidades():
    try:
        # Analiza el Oro (Refugio) y el Cobre/Litio (Energía)
        oro = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        litio = yf.Ticker("LIT").history(period="1d")['Close'].iloc[-1]
        
        # Aquí simulamos el análisis de productos ganadores (E-commerce)
        # En una fase avanzada, aquí conectaremos con Google Trends
        return {
            "oro": round(oro, 2),
            "litio": round(litio, 2),
            "sugerencia": "🔱 ALERTA VMAX: Demanda de paneles solares portátiles subiendo. Margen estimado: 40%."
        }
    except:
        return {"oro": "N/D", "litio": "N/D", "sugerencia": "Analizando mercado..."}

# --- DASHBOARD DE CONTROL TOTAL ---
@app.route('/')
def dashboard():
    datos = buscar_oportunidades()
    with sqlite3.connect(DB_PATH) as conn:
        leads = conn.execute('SELECT * FROM leads ORDER BY fecha DESC LIMIT 10').fetchall()
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>VOLTAMAXPRO - VISIONARY CONTROL</title>
        <style>
            body {{ background: #000; color: #0f0; font-family: 'Courier New', monospace; padding: 20px; }}
            .panel {{ border: 2px solid #0f0; padding: 15px; margin-bottom: 20px; border-radius: 10px; }}
            h1 {{ text-align: center; color: #fff; text-shadow: 0 0 10px #0f0; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .btn {{ background: #0f0; color: #000; padding: 10px; text-decoration: none; font-weight: bold; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>🔱 VOLTAMAXPRO - CENTRO DE MANDO 🔱</h1>
        
        <div class="grid">
            <div class="panel">
                <h2>📈 MERCADO Y FINANZAS</h2>
                <p>ORO (Refugio): ${datos['oro']} USD</p>
                <p>LITIO (Energía): ${datos['litio']} USD</p>
                <p style="color: #ff0;">{datos['sugerencia']}</p>
            </div>
            
            <div class="panel">
                <h2>🛍️ E-COMMERCE ESTRATÉGICO</h2>
                <p>Tienda: VoltamaxPro Shopify</p>
                <p>Estado: Analizando productos ganadores...</p>
                <a href="/registro" class="btn">VER LINK DE CAPTACIÓN</a>
            </div>
        </div>

        <div class="panel">
            <h2>👥 ÚLTIMOS SOCIOS CLUB VIP (LEADS)</h2>
            <table style="width:100%">
                <tr><th>Nombre</th><th>WhatsApp</th><th>Interés</th><th>Fecha</th></tr>
                {''.join(f"<tr><td>{l[0]}</td><td>{l[1]}</td><td>{l[2]}</td><td>{l[3]}</td></tr>" for l in leads)}
            </table>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# --- PORTAL DE CAPTACIÓN (LEAD MAGNET) ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        wa = request.form['whatsapp']
        interes = request.form['interes']
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('INSERT INTO leads VALUES (?, ?, ?, ?)', (nombre, wa, interes, datetime.now()))
        return "<h1>🔱 ¡Bienvenido al Club VMAX! Pronto recibirás ofertas millonarias.</h1>"
    
    return '''
        <body style="background:#000; color:#0f0; font-family:sans-serif; text-align:center;">
            <h1>🔱 ÚNETE AL CLUB VIP VOLTAMAXPRO 🔱</h1>
            <p>Obtén descuentos exclusivos y productos ganadores antes que nadie.</p>
            <form method="post">
                <input name="nombre" placeholder="Tu Nombre" required><br><br>
                <input name="whatsapp" placeholder="WhatsApp (con código)" required><br><br>
                <select name="interes">
                    <option value="Baterías">Baterías/Energía</option>
                    <option value="Inversiones">Inversiones/Club</option>
                    <option value="Bienes Raices">Bienes Raíces</option>
                </select><br><br>
                <button type="submit" style="background:#0f0; padding:10px 20px;">REGISTRARME</button>
            </form>
        </body>
    '''

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
