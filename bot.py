import os
from flask import Flask, request
import requests

app = Flask(_name_)

# Configuración de variables (las que ya tienes en Render)
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
                    
                    # --- DICCIONARIO DE INTELIGENCIA DEL BOT ---
                    
                    # 1. Saludos
                    if any(word in user_text for word in ["hola", "buenas", "que tal"]):
                        answer = "👋 ¡Hola! Soy el asistente de Volta MaxPro. ¿En qué puedo ayudarte hoy? \n\nPuedes preguntarme por: 'precios', 'stock', 'tienda' o 'whatsapp'."

                    # 2. Precios y Cuánto cuesta
                    elif any(word in user_text for word in ["precio", "cuanto", "vale", "costo", "valor"]):
                        answer = "💰 Los precios de nuestros productos de MaxPro varían. Puedes ver el catálogo con precios actualizados aquí: https://vmaxpro.com/precios"

                    # 3. Stock y Disponibilidad
                    elif any(word in user_text for word in ["queda", "stock", "disponible", "hay"]):
                        answer = "📦 ¡Hola! El stock vuela. Para asegurarte de que aún queda el modelo que quieres, revísalo aquí en tiempo real: https://vmaxpro.com/stock"

                    # 4. Enlace a la Tienda
                    elif any(word in user_text for word in ["tienda", "link", "web", "pagina"]):
                        answer = "🛒 Nuestra tienda oficial es: https://vmaxpro.com \n¡Hacemos envíos rápidos!"

                    # 5. Contacto Humano / WhatsApp
                    elif any(word in user_text for word in ["whatsapp", "contacto", "hablar con alguien", "telefono"]):
                        answer = "📱 ¡Claro! Si prefieres hablar con una persona, escríbenos al WhatsApp: https://wa.me/tu_numero_aqui"

                    # 6. Información General
                    elif "info" in user_text or "informacion" in user_text:
                        answer = "ℹ️ En Volta MaxPro somos especialistas en tecnología de alto rendimiento. Escribe 'tienda' para ver los productos o 'precios' para saber más."

                    # 7. Si no entiende nada (Respuesta de seguridad)
                    else:
                        answer = "🤔 No estoy seguro de haberte entendido bien, pero escribe 'ayuda' o 'info' para ver las opciones que tengo para ti. 🚀"
                    
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
