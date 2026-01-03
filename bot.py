import os, sqlite3, requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- VARIABLES ---
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

# --- 🛰️ LA PIEZA QUE TE FALTA: EL DASHBOARD ---
@app.route('/')
def dashboard_principal():
    # Esta función crea la página que ahora te da error 404
    return render_template_string("""
        <body style="background:#000; color:#0f0; font-family:monospace; padding:30px; text-align:center;">
            <h1 style="border:2px solid #0f0; padding:10px;">🔱 VMAX - CENTRO DE MANDO ACTIVO</h1>
            <p>El servidor de Frankfurt está operando correctamente.</p>
            <div style="background:#111; border:1px solid #333; padding:20px; margin-top:20px;">
                <h3>SISTEMA ONLINE</h3>
                <p>Esperando mensajes de Facebook para registrar datos...</p>
            </div>
        </body>
    """)

# --- TU WEBHOOK (Lo que ya tienes) ---
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Error de Verificación", 403

if __name__ == "__main__":
    # Render usa el puerto 10000 como se ve en tu imagen 7
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
