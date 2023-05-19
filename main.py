import os
from flask import Flask, request
from telegram.bot import Bot
from helper.music import search, download_audio
from helper.common import commands , resolve

app = Flask(__name__)
bot = Bot(os.getenv('TELEGRAM_BOT'))
state = True

@app.route('/', methods=['POST'])
def telegram():
    # Retrieve message details from the request
    sender_id , text = resolve(request.get_json())
    
    global state
    print(state)
    if not state :
        if text == '/on':
            state = True
        else:
            return 'OK', 200
   
    send = commands(text)
    if send != 0:
        bot.send_message(sender_id, send)
        return 'OK', 200
    
    # Search for music and retrieve necessary information
    title, url, duration= search(text)
    
    # If no URL found, send the title and return "Fail"
    if not url:
        bot.send_message(sender_id, title)
        return 'Fail', 200
    
    # Send the title, duration, and URL as a message
    bot.send_message(sender_id, f"{title}\n\n{duration}\n\n{url}")
    
    # Download the audio file
    response, audio_file , thumbnail= download_audio(url)
    
    if not audio_file:
        # If audio file download fails, send the response message and return "Fail"
        bot.send_message(sender_id, response)
        return 'Fail', 200
    
    # Send the thumbnail, the downloaded audio file with the title as the caption
    bot.send_photo(sender_id, thumbnail, caption=title)
    with open(audio_file, 'rb') as f:
        bot.send_audio(sender_id, f, caption=title)
    
    return 'OK', 200
