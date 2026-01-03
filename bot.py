import os, sqlite3, requests
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
DB_PATH = "/opt/render/project/src/vmax_data.db" # Ruta absoluta para Render

def init_db():
    # Esta función asegura que el "cuaderno" exista sí o sí
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS leads (id TEXT, msg TEXT, fecha TEXT)')
        conn.commit()

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
                    
                    init_db() # Nos aseguramos que la tabla existe antes de guardar
                    with sqlite3.connect(DB_PATH) as conn:
                        conn.execute('INSERT INTO leads VALUES (?, ?, ?)', (uid, msg, fecha))
    return "ok", 200

@app.route('/')
def dashboard():
    try:
        init_db() # Aseguramos la tabla antes de leer
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            leads = conn.execute("SELECT * FROM leads ORDER BY rowid DESC").fetchall()
        
        return render_template_string("""
            <body style="background:#000; color:#0f0; font-family:monospace; padding:30px;">
                <h1 style="border:2px solid #0f0; padding:15px; text-align:center;">🔱 VMAX - CONTROL REAL</h1>
                <div style="margin-top:20px;">
                    {% if not leads %}
                        <p style="color:red; text-align:center;">SISTEMA CONECTADO: Esperando mensaje de prueba...</p>
                    {% endif %}
                    {% for l in leads %}
                    <div style="border:1px solid #333; padding:10px; margin-bottom:10px; background:#111;">
                        <b>ID: {{l.id}}</b> | <span style="color:#888;">{{l.fecha}}</span><br>
                        <span style="color:yellow;">MENSAJE:</span> {{l.msg}}
                    </div>
                    {% endfor %}
                </div>
            </body>
        """, leads=leads)
    except Exception as e:
        return f"Error en el sistema: {str(e)}"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Error", 403

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
