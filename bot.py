from flask import Flask, request

app = Flask("vmaxpro")

@app.route('/webhook', methods=['GET'])
def verify():
    return request.args.get("hub.challenge", "Error"), 200

@app.route('/')
def home():
    return "Bot Online"

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=10000)
