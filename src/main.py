import os
from flask import Flask, request
import telebot
from helper.music import search, download_audio

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT'), threaded=False)
state = False


@app.route('/', methods=['POST'])
def telegram():
    # Process incoming updates
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200


@bot.message_handler(commands=['start'])
def handle_start(message):
    # Handle the /start command
    bot.reply_to(message, "Hello there! I am MusicBot, your personal music assistant.\nTo find any song or audio, simply send me the title you want to search for.")


@bot.message_handler(commands=['help'])
def handle_help(message):
    # Handle the /help command
    bot.reply_to(message, "MusicBot Help:\n\nSend me the title or description of a song or audio you want to find, and I will fetch it for you.")


@bot.message_handler(commands=['on'])
def handle_on(message):
    global state
    state = True
    # Handle the /on command
    bot.reply_to(message, "BOT ON")


@bot.message_handler(commands=['off'])
def handle_off(message):
    global state
    state = False
    # Handle the /off command
    bot.reply_to(message, "BOT OFF")


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    if not state:
        return

    query = message.text
    title, url, duration = search(query)

    if not url:
        # No URL found, reply with the title
        bot.reply_to(message, title)
        return
    else:
        # Download audio file
        wait = bot.reply_to(message, 'Downloading...')
        response, audio_file, thumbnail = download_audio(url)
        bot.delete_message(message.chat.id, wait.message_id)

        if not audio_file:
            # Error downloading audio file
            bot.reply_to(message, response)
            return
        else:
            try:
                # Send photo with caption
                bot.send_photo(message.chat.id, thumbnail, caption=f"{title}\n\n{duration}\n\n{url}",
                               reply_to_message_id=message.message_id)
            except:
                # Send message with caption
                bot.reply_to(message, f"{title}\n\n{duration}\n\n{url}")

            # Send audio file
            with open(audio_file, 'rb') as f:
                bot.send_audio(message.chat.id, f, caption=title)


if __name__ == '__main__':
    app.run()
