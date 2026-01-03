import os, sqlite3, time, requests, threading
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- VARIABLES DE RENDER (Imagen 1000300013.jpg) ---
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
DB_PATH = "vmax_data.db"

# --- INICIALIZAR BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS leads (id TEXT PRIMARY KEY, msg TEXT, fecha TIMESTAMP)')
    conn.commit()
    conn.close()

# --- WEBHOOK (Para Facebook) ---
@app.route('/webhook', methods=['GET'])
def verify():
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
                    uid = event["sender"]["id"]
                    msg = event["message"].get("text", "")
                    # Guardar el mensaje automáticamente en el Dashboard
                    with sqlite3.connect(DB_PATH) as conn:
                        conn.execute('INSERT OR REPLACE INTO leads VALUES (?, ?, ?)', (uid, msg, datetime.now()))
    return "ok", 200

# --- 🛰️ TU DASHBOARD (La ruta que te falta para ver resultados) ---
@app.route('/dashboard')
def dashboard():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        leads = conn.execute("SELECT * FROM leads ORDER BY fecha DESC LIMIT 20").fetchall()
    
    return render_template_string("""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:20px; text-align:center;">
            <h1 style="border: 2px solid #0f0; padding:10px;">🔱 VMAX - CENTRO DE MANDO</h1>
            <div style="margin-top:20px; border: 1px solid #333; padding:15px; background:#111;">
                <h3>📥 ÚLTIMOS LEADS DE FACEBOOK</h3>
                <hr style="border-color:#333;">
                {% if not leads %}
                    <p>Esperando el primer mensaje... Escríbele a tu página para probar.</p>
                {% endif %}
                {% for l in leads %}
                <p style="text-align:left;">📍 {{ l.fecha }} | <b>ID:</b> {{ l.id }} | <b>MSG:</b> {{ l.msg }}</p>
                {% endfor %}
            </div>
            <p style="margin-top:30px; color:#555;">Estado: ONLINE - Frankfurt Node</p>
        </body>
    """, leads=leads)

# --- INICIO DEL SERVIDOR (Imagen 1000300031.jpg) ---
if __name__ == "__main__":
    init_db()
    # Usamos el puerto 10000 que tienes en tus variables de entorno
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
