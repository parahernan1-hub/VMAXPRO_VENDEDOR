from flask import Flask, request

app = Flask(_name_)

@app.route('/webhook', methods=['GET'])
def verify():
    # Este es el token que usaremos luego en Meta
    token = "vmax2025"
    if request.args.get("hub.verify_token") == token:
        return request.args.get("hub.challenge")
    return "Error de token", 403

@app.route('/')
def home():
    return "Servidor de VmaxPro Activo"

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=10000)
