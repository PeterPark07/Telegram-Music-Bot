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
    
    title , url , duration , thumbnail, thumbnail2= search(text)
    
    if not url:
        bot.send_message(sender_id, title)
        return 'Fail' , 200
    
    message_text = f"{title}\n\n {duration}\n\n {url}"
    bot.send_message(sender_id, message_text)
    
    try:
        bot.send_photo(sender_id, thumbnail, caption=title)
    except Exception as e:
        try:
            bot.send_photo(sender_id, thumbnail2, caption=title)
        except Exception as e:
            bot.send_message(sender_id, "No thumbnail available.")
            return 'Fail', 200
    
    response, audio_file = download_audio(url)
    
    if not audio_file :
        bot.send_message(sender_id, response)
        return 'Fail' , 200

    with open(audio_file, 'rb') as f:
        bot.send_audio(sender_id, f , caption = title)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
