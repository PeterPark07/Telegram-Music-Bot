from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'OK', 200

@app.route('/download', methods=['POST', 'GET'])
def telegram():

    message = request.get_json()['message']
    
    sender_id = message['from']['id']
    text = message['text']
    
    sendMessage(sender_id, text)
    
    return 'OK', 200
