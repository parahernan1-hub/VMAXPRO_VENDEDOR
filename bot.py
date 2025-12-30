import os
from flask import Flask, request
import requests

app = Flask(_name_)

# Configuración de variables
ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args.get("hub.challenge"), 200
    return "Bot de Volta en línea", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    user_text = messaging_event["message"].get("text").lower()
                    
                    if any(word in user_text for word in ["hola", "buenas"]):
                        answer = "👋 ¡Hola! Soy el asistente de Volta MaxPro. ¿En qué puedo ayudarte?"
                    elif any(word in user_text for word in ["precio", "cuanto"]):
                        answer = "💰 Puedes ver los precios aquí: https://vmaxpro.com/precios"
                    elif "tienda" in user_text:
                        answer = "🛒 Nuestra tienda: https://vmaxpro.com"
                    else:
                        answer = "Escribe 'hola' para empezar. 🚀"
                    
                    send_message(sender_id, answer)
    return "ok", 200

def send_message(recipient_id, message_text):
    params = {"access_token": ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    requests.post("https://graph.facebook.com/v12.0/me/messages", params=params, headers=headers, json=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
