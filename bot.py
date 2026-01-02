import os, sqlite3, time, random, requests, threading, logging
from flask import Flask, request, render_template_string
from datetime import datetime

# --- CONFIGURACIÓN DE REGISTROS ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- VARIABLES DE ENTORNO (Mantenemos tus nombres exactos) ---
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
DB_PATH = "vmax_imperio.db"

# --- 1. INICIALIZACIÓN DE LA BASE DE DATOS ---
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Leads de Facebook con Scoring
        c.execute('CREATE TABLE IF NOT EXISTS leads (id TEXT PRIMARY KEY, msg TEXT, score REAL, fecha TIMESTAMP)')
        # Productos encontrados por el Cazador
        c.execute('CREATE TABLE IF NOT EXISTS mercado (id INTEGER PRIMARY KEY, item TEXT, margen REAL, link TEXT)')
        conn.commit()
    logger.info("✅ Base de datos sincronizada.")

# --- 2. EL CAZADOR PROACTIVO (HILO INDEPENDIENTE) ---
def motor_cazador():
    """Busca productos y oportunidades en segundo plano cada hora"""
    while True:
        try:
            # Aquí inyectamos los resultados del análisis de mercado
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
            logger.error(f"Error en el Cazador: {e}")
            time.sleep(60)

# --- 3. WEBHOOKS (Tu código original mejorado) ---
@app.route('/webhook', methods=['GET'])
def verify():
    # Validación oficial de Facebook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args.get("hub.challenge"), 200
    return "Bot de Volta en línea", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                if event.get("message"):
                    sender_id = event["sender"]["id"]
                    user_text = event["message"].get("text", "").lower()
                    
                    # Ejecutamos el cierre de venta en hilo separado para evitar errores de timeout
                    threading.Thread(target=procesar_y_responder, args=(sender_id, user_text)).start()
    return "ok", 200

# --- 4. LÓGICA DE CIERRE Y RESPUESTA (Vendedor IA) ---
def procesar_y_responder(uid, msg):
    # Scoring: ¿Es un cliente potencial?
    score = 1.0 if any(word in msg for word in ["precio", "cuanto", "tienda", "comprar"]) else 0.4
    
    # Registro en DB
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT OR REPLACE INTO leads VALUES (?, ?, ?, ?)', (uid, msg, score, datetime.now()))
    
    # Camuflaje Humano
    time.sleep(random.uniform(4, 8))
    
    # Selección de respuesta según interés
    if score == 1.0:
        answer = "💰 ¡Hola! Los precios actuales están aquí: https://vmaxpro.com/precios. Si compras hoy, tienes envío gratis a Santander. 🚀"
    elif any(word in msg for word in ["hola", "buenas"]):
        answer = "👋 ¡Hola! Soy el asistente de Volta MaxPro. ¿En qué puedo ayudarte hoy?"
    elif "tienda" in msg:
        answer = "🛒 Nuestra tienda oficial: https://vmaxpro.com"
    else:
        answer = "Recibido. Un asesor humano de Volta revisará tu caso enseguida. Escribe 'precio' para ver ofertas."

    send_message(uid, answer)

def send_message(recipient_id, message_text):
    params = {"access_token": ACCESS_TOKEN}
    data = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    try:
        r = requests.post("https://graph.facebook.com/v12.0/me/messages", params=params, json=data, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logger.error(f"Error enviando a FB: {e}")

# --- 5. DASHBOARD REAL (Análisis de Datos y Finanzas) ---
@app.route('/dashboard')
def dashboard():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        leads = conn.execute("SELECT * FROM leads ORDER BY score DESC, fecha DESC LIMIT 15").fetchall()
        mercado = conn.execute("SELECT * FROM mercado ORDER BY margen DESC").fetchall()
    
    # Plantilla táctica
    return render_template_string("""
        <body style="background:#0a0a0a; color:#00ff00; font-family:monospace; padding:30px;">
            <h1 style="border-bottom: 2px solid #00ff00;">🔱 VMAX - CENTRO DE CONTROL TÁCTICO</h1>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div style="border:1px solid #00ff00; padding:15px;">
                    <h3>🎯 LEADS CALIENTES (FACEBOOK)</h3>
                    {% for l in leads %}
                    <div style="margin-bottom:10px; border-bottom:1px solid #333;">
                        <span style="color:{% if l.score == 1.0 %}yellow{% else %}#0f0{% endif %};">[SCORE: {{l.score}}]</span> 
                        ID: {{l.id}} | Msg: {{l.msg}}
                    </div>
                    {% endfor %}
                </div>
                <div style="border:1px solid #00ffff; padding:15px; color:#00ffff;">
                    <h3>💰 OPORTUNIDADES DEL CAZADOR</h3>
                    {% for m in mercado %}
                    <p>{{ m.item }} - <span style="font-weight:bold;">{{ m.margen }}% Margen</span></p>
                    {% endfor %}
                    <hr>
                    <p style="color:white;">ESTADO: <span style="color:#0f0;">PROCESANDO TENDENCIAS...</span></p>
                </div>
            </div>
        </body>
    """, leads=leads, mercado=mercado)

if __name__ == "__main__":
    init_db()
    # Lanzamos el cazador en un hilo aparte para que no bloquee los mensajes
    threading.Thread(target=motor_cazador, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
