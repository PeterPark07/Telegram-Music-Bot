from flask import Flask, request

from helper.music import search , download , delete
from helper.telegram import sendMessage , sendAudio

app = Flask(__name__)

@app.route('/')
def home():
    return 'OK', 200

@app.route('/download', methods=['POST', 'GET'])
def telegram():

    message = request.get_json()['message']
    sender_id = message['from']['id']
    text = message['text']
    
    response , url = search(text)
    
    sendMessage(sender_id, response)
    
    if not url:
        return 'Fail' , 200
    
    response , audio_url , name = download_audio(url)
    
    if not audio_url :
        sendMessage(sender_id, response)
        return 'Fail' , 200
    
    sendMessage(sender_id, str(audio_url))
    sendAudio(sender_id, audio_url , name)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
