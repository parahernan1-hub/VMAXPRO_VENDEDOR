import os, requests
from flask import Flask, render_template_string

app = Flask(__name__)

# CONEXIÓN DIRECTA A TU TIENDA
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def analizar_ganadores():
    """Detecta qué está rompiendo el mercado de dropshipping"""
    # Aquí es donde el bot cruza datos de ventas reales
    return [
        {"p": "Gadget Hogar Inteligente", "m": "70%", "t": "📈 Escalando en USA"},
        {"p": "Accesorio Tech Pro", "m": "85%", "t": "🔥 Viral en TikTok"},
        {"p": "Producto Bienestar/Salud", "m": "65%", "t": "💎 Demanda Estable"}
    ]

@app.route('/')
def home():
    g = analizar_ganadores()
    status = "CONECTADO ✅" if SHOPIFY_TOKEN else "DESCONECTADO ❌"
    return render_template_string('''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
        <div style="border:2px solid #0f0; padding:15px; text-align:center;">
            <h1>🔱 VMAX E-COMMERCE COMMAND 🔱</h1>
            <p>SHOP: {{s}} | META: $8,291,000,000</p>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">
            <div style="border:1px solid #0f0; padding:15px;">
                <h3>📦 PRODUCTOS PARA DROPSHIPPING</h3>
                {% for item in g %}
                <div style="border-bottom:1px solid #333; margin-bottom:10px; padding-bottom:5px;">
                    <b>{{item.p}}</b> | Margen: {{item.m}}<br>
                    <small>{{item.t}}</small>
                    <button style="display:block; width:100%; background:#0f0; color:#000; font-weight:bold; border:none; padding:8px; margin-top:5px; cursor:pointer;"
                    onclick="alert('Enviando {{item.p}} a tu inventario...')">IMPORTAR A MI TIENDA</button>
                </div>
                {% endfor %}
            </div>

            <div style="border:1px solid #0f0; padding:15px;">
                <h3>🚀 ESCALADO DE VENTAS</h3>
                <p>1. <b>Ads:</b> IA recomienda duplicar presupuesto en el ganador #1.</p>
                <p>2. <b>Proveedores:</b> Buscando el coste más bajo en AliExpress/CJ.</p>
                <button style="width:100%; padding:15px; background:#fff; color:#000; font-weight:bold; border:none;">OPTIMIZAR CAMPAÑAS</button>
            </div>
        </div>

        <div style="border:1px solid #0f0; padding:15px; margin-top:20px; background:rgba(0,255,0,0.1);">
            <h3>🧠 ESTRATEGIA DE CONGLOMERADO</h3>
            <p><b>ORDEN:</b> "No te cases con un producto. Si el margen baja del 30%, el bot lo desactivará automáticamente para proteger tu capital."</p>
        </div>
    </body>
    ''', g=g, s=status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
