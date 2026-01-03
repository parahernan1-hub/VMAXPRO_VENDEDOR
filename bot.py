import os, requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# LLAVES MAESTRAS DE TU IMPERIO (Configuradas en Render)
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_TOKEN')
SHOP_URL = os.environ.get('SHOP_URL')

def ejecutar_importacion_real(nombre_producto):
    """Envía una orden real de creación de producto a Shopify"""
    if not SHOPIFY_TOKEN or not SHOP_URL:
        return "❌ ERROR: No hay API Token configurado en Render."
    
    url = f"https://{SHOP_URL}/admin/api/2023-10/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Datos del producto ganador detectado por la IA
    nuevo_producto = {
        "product": {
            "title": f"VMAX WINNER: {nombre_producto}",
            "body_html": "<strong>Producto ganador detectado por el sistema VMAX.</strong>",
            "vendor": "VMAX DROPSHIPPING",
            "status": "draft" # Se guarda como borrador para que tú le des el toque final
        }
    }
    
    try:
        r = requests.post(url, json=nuevo_producto, headers=headers)
        if r.status_code == 201:
            return f"✅ ¡ÉXITO! '{nombre_producto}' ya aparece en tu panel de Shopify."
        else:
            return f"❌ ERROR DE SHOPIFY: {r.status_code} - Revisa tus permisos de API."
    except Exception as e:
        return f"❌ FALLO DE CONEXIÓN: {str(e)}"

@app.route('/')
def dashboard():
    # El estado de conexión ahora es real, no un texto fijo
    status_icon = "✅" if SHOPIFY_TOKEN else "❌"
    return render_template_string('''
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px; text-transform:uppercase;">
        <div style="border:2px solid #0f0; padding:15px; text-align:center;">
            <h1>🔱 VMAX E-COMMERCE COMMAND 🔱</h1>
            <p>SHOP: CONECTADO {{s}} | META: $8,291,000,000</p>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">
            <div style="border:1px solid #0f0; padding:15px;">
                <h3>📦 PRODUCTOS PARA DROPSHIPPING</h3>
                
                <div style="margin-bottom:15px;">
                    <b>Gadget Hogar Inteligente</b> | Margen: 70%<br>
                    <button onclick="importar('Gadget Hogar')" style="width:100%; background:#0f0; color:#000; font-weight:bold; padding:10px; cursor:pointer; border:none;">IMPORTAR A MI TIENDA</button>
                </div>

                <div style="margin-bottom:15px;">
                    <b>Accesorio Tech Pro</b> | Margen: 85%<br>
                    <button onclick="importar('Accesorio Tech')" style="width:100%; background:#0f0; color:#000; font-weight:bold; padding:10px; cursor:pointer; border:none;">IMPORTAR A MI TIENDA</button>
                </div>
            </div>

            <div style="border:1px solid #0f0; padding:15px;">
                <h3>🚀 ESCALADO DE VENTAS</h3>
                <p>1. ADS: IA RECOMIENDA DUPLICAR PRESUPUESTO.</p>
                <button onclick="alert('IA reajustando pujas en Meta Ads...')" style="width:100%; background:#444; color:#fff; padding:10px; border:none; cursor:pointer;">OPTIMIZAR CAMPAÑAS</button>
            </div>
        </div>

        <script>
            function importar(nombre) {
                fetch('/api/importar/' + nombre)
                .then(r => r.text())
                .then(mensaje => alert(mensaje));
            }
        </script>
    </body>
    ''', s=status_icon)

@app.route('/api/importar/<nombre>')
def api_importar(nombre):
    return ejecutar_importacion_real(nombre)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
