import os
from flask import Flask, request
from telegram.bot import Bot
from helper.music import search, download_audio

app = Flask(__name__)
bot = Bot(os.getenv('TELEGRAM_BOT'))

@app.route('/', methods=['POST'])
def telegram():
    # Retrieve message details from the request
    message = request.get_json()['message']
    sender_id = message['from']['id']
    text = message['text']
    
    if text == '/start':
        bot.send_message(sender_id, "Hello there! I am MusicBot, your personal music assistant. To find any song or audio, simply send me the title you want to search for.")
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
    
    bot.send_message(sender_id, thumbnail)
    try:
        bot.send_document(sender_id, thumbnail, caption=title)
    except:
        l = 1
    
    if not audio_file:
        # If audio file download fails, send the response message and return "Fail"
        bot.send_message(sender_id, response)
        return 'Fail', 200

    # Send the downloaded audio file with the title as the caption
    with open(audio_file, 'rb') as f:
        bot.send_audio(sender_id, f, caption=title)
    
    return 'OK', 200
