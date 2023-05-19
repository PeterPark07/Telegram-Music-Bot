import os
from flask import Flask, request
from telegram.bot import Bot

from helper.music import search , download_audio

app = Flask(__name__)

# Create a Telegram bot
bot = Bot(os.getenv('TELEGRAM_BOT'))

@app.route('/')
def home():
    return 'OK', 200

@app.route('/download', methods=['POST', 'GET'])
def telegram():

    message = request.get_json()['message']
    sender_id = message['from']['id']
    text = message['text']
    
    audio , url = search(text)
    
    bot.send_message(sender_id, audio)
    bot.send_message(sender_id, url)
    
    if not url:
        bot.send_message(sender_id, 'Could not download')
        return 'Fail' , 200
    
    response , audio_file = download_audio(url)
    
    if not audio_file :
        bot.send_message(sender_id, response)
        return 'Fail' , 200
    
    bot.send_message(sender_id, str(audio_file))
    with open(audio_file, 'rb') as f:
        bot.send_audio(sender_id, f)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
