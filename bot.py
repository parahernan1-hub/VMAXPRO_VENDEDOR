import os, sqlite3, time, random, requests, threading, logging
from flask import Flask, request, render_template_string
from datetime import datetime

# --- CONFIGURACIÓN DE REGISTROS ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- VARIABLES DE ENTORNO ---
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
DB_PATH = "vmax_imperio.db"

# --- 1. INICIALIZACIÓN DE LA BASE DE DATOS ---
def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS leads (id TEXT PRIMARY KEY, msg TEXT, score REAL, fecha TIMESTAMP)')
            c.execute('CREATE TABLE IF NOT EXISTS mercado (id INTEGER PRIMARY KEY, item TEXT, margen REAL, link TEXT)')
            conn.commit()
        logger.info("✅ Base de datos sincronizada.")
    except Exception as e:
        logger.error(f"Error DB: {e}")

# --- 2. EL CAZADOR PROACTIVO ---
def motor_cazador():
    while True:
        try:
            oportunidades = [
                ("VMax Cooler Pro", 65.4, "https://vmaxpro.com/shop1"),
                ("Batería Litio Max", 42.1, "https://vmaxpro.com/shop2"),
                ("Inmueble Santander Urgente", 15.0, "https://idealista.com/chollos")
            ]
            with sqlite3.connect(DB_PATH) as conn:
                for item, margen, link in oportunidades:
                    conn.execute('INSERT OR IGNORE INTO mercado (item, margen, link) VALUES (?, ?, ?)', (item, margen, link))
            time.sleep(3600) 
        except Exception as e:
            time.sleep(60)

# --- 3. WEBHOOKS ---
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
    return "Bot de Volta en línea", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and data.get("object") == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                if event.get("message"):
                    sender_id = event["sender"]["id"]
                    user_text = event["message"].get("text", "").lower()
                    threading.Thread(target=procesar_y_responder, args=(sender_id, user_text)).start()
    return "ok", 200

# --- 4. LÓGICA DE CIERRE ---
def procesar_y_responder(uid, msg):
    score = 1.0 if any(word in msg for word in ["precio", "cuanto", "tienda", "comprar"]) else 0.4
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT OR REPLACE INTO leads VALUES (?, ?, ?, ?)', (uid, msg, score, datetime.now()))
    
    time.sleep(random.uniform(2, 5))
    
    if score == 1.0:
        answer = "💰 ¡Hola! Los precios actuales están aquí: https://vmaxpro.com/precios. Envío gratis a Santander hoy. 🚀"
    else:
        answer = "👋 ¡Hola! Soy el asistente de Volta. ¿En qué puedo ayudarte?"

    params = {"access_token": ACCESS_TOKEN}
    requests.post("https://graph.facebook.com/v12.0/me/messages", params=params, json={"recipient": {"id": uid}, "message": {"text": answer}})

# --- 5. DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            leads = conn.execute("SELECT * FROM leads ORDER BY score DESC, fecha DESC LIMIT 15").fetchall()
            mercado = conn.execute("SELECT * FROM mercado ORDER BY margen DESC").fetchall()
        
        return render_template_string("""
            <body style="background:#0a0a0a; color:#00ff00; font-family:monospace; padding:30px;">
                <h1>🔱 VMAX - CONTROL TÁCTICO</h1>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                    <div style="border:1px solid #00ff00; padding:15px;">
                        <h3>🎯 LEADS FACEBOOK</h3>
                        {% for l in leads %}
                        <p>[{{l.score}}] {{l.id}}: {{l.msg}}</p>
                        {% endfor %}
                    </div>
                    <div style="border:1px solid #00ffff; padding:15px; color:#00ffff;">
                        <h3>💰 MERCADO</h3>
                        {% for m in mercado %}
                        <p>{{ m.item }} - {{ m.margen }}%</p>
                        {% endfor %}
                    </div>
                </div>
            </body>
        """, leads=leads, mercado=mercado)
    except Exception as e:
        return f"Error en Dashboard: {e}"

if __name__ == "__main__":
    init_db()
    threading.Thread(target=motor_cazador, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
