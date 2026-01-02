import os, sqlite3, time, random, requests, threading
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- VARIABLES (Cargadas de Render) ---
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
DB_PATH = "vmax_data.db"

# --- INICIALIZAR BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS leads (id TEXT PRIMARY KEY, msg TEXT, fecha TIMESTAMP)')
    conn.commit()
    conn.close()

# --- TU RUTA DE VERIFICACIÓN (Imagen 1) ---
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Bot de Volta Online", 200

# --- TU RUTA DE MENSAJES ---
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and data.get("object") == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                if event.get("message"):
                    uid = event["sender"]["id"]
                    msg = event["message"].get("text", "")
                    # Guardar lead
                    with sqlite3.connect(DB_PATH) as conn:
                        conn.execute('INSERT OR REPLACE INTO leads VALUES (?, ?, ?)', (uid, msg, datetime.now()))
    return "ok", 200

# --- 🛰️ LA RUTA QUE TE FALTA (DASHBOARD) ---
@app.route('/dashboard')
def dashboard():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        leads = conn.execute("SELECT * FROM leads ORDER BY fecha DESC LIMIT 20").fetchall()
    
    return render_template_string("""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
            <h1>🔱 VMAX DASHBOARD</h1>
            <h3>ÚLTIMOS LEADS CAPTURADOS:</h3>
            {% for l in leads %}
            <p>{{ l.fecha }} | ID: {{ l.id }} | MSG: {{ l.msg }}</p>
            {% endfor %}
        </body>
    """, leads=leads)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
