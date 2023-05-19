import os
from flask import Flask, request
from telegram.bot import Bot
from helper.music import search, download_audio

app = Flask(__name__)
bot = Bot(os.getenv('TELEGRAM_BOT'))

@app.route('/download', methods=['POST'])
def telegram():
    # Retrieve message details from the request
    message = request.get_json()['message']
    sender_id = message['from']['id']
    text = message['text']
    
    # Search for music and retrieve necessary information
    title, url, duration, thumbnail, thumbnail2 = search(text)
    
    # If no URL found, send the title and return "Fail"
    if not url:
        bot.send_message(sender_id, title)
        return 'Fail', 200
    
    # Send the title, duration, and URL as a message
    bot.send_message(sender_id, f"{title}\n\n{duration}\n\n{url}")
    
    try:
        # Attempt to send the thumbnail with the title as the caption
        bot.send_photo(sender_id, thumbnail, caption=title)
    except Exception as e:
        try:
            bot.send_photo(sender_id, thumbnail2, caption=title)
        except Exception as e:
            # If fail, send a message indicating no thumbnail is available
            bot.send_message(sender_id, "No thumbnail available.")
    
    # Download the audio file
    response, audio_file = download_audio(url)
    
    if not audio_file:
        # If audio file download fails, send the response message and return "Fail"
        bot.send_message(sender_id, response)
        return 'Fail', 200

    # Send the downloaded audio file with the title as the caption
    with open(audio_file, 'rb') as f:
        bot.send_audio(sender_id, f, caption=title)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
