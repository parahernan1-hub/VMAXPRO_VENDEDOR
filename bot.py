import os, sqlite3, requests, threading
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
DB_PATH = "vmax_data.db"

# --- 1. MEMORIA REAL (Base de Datos) ---
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS leads (id TEXT, msg TEXT, fecha TEXT)')
        conn.commit()

# --- 2. RECEPTOR DE MENSAJES (Facebook) ---
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and data.get("object") == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                if event.get("message"):
                    uid = event["sender"]["id"]
                    msg = event["message"].get("text", "")
                    fecha = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
                    
                    # GUARDADO REAL: Aquí es donde deja de ser simulación
                    with sqlite3.connect(DB_PATH) as conn:
                        conn.execute('INSERT INTO leads VALUES (?, ?, ?)', (uid, msg, fecha))
                    
                    # Opcional: Responder automáticamente
                    enviar_respuesta(uid, "🔱 Recibido. Un asesor de VMax revisará tu mensaje pronto.")
    return "ok", 200

def enviar_respuesta(uid, texto):
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={ACCESS_TOKEN}"
    payload = {"recipient": {"id": uid}, "message": {"text": texto}}
    requests.post(url, json=payload)

# --- 3. EL DASHBOARD (Ya no está vacío, lee la memoria) ---
@app.route('/')
def dashboard():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        leads = conn.execute("SELECT * FROM leads ORDER BY rowid DESC").fetchall()
    
    return render_template_string("""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
            <h1 style="border:2px solid #0f0; padding:15px; text-align:center;">🔱 VMAX - CONTROL DE LEADS REAL</h1>
            <div style="margin-top:20px;">
                {% if not leads %}
                    <p style="color:red; text-align:center;">SISTEMA VACÍO: Esperando el primer mensaje real...</p>
                {% endif %}
                {% for l in leads %}
                <div style="border:1px solid #333; padding:10px; margin-bottom:10px; background:#111;">
                    <span style="color:#888;">[{{l.fecha}}]</span> <b>ID: {{l.id}}</b><br>
                    <span style="color:yellow;">MENSAJE:</span> {{l.msg}}
                </div>
                {% endfor %}
            </div>
        </body>
    """, leads=leads)

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Error", 403

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
