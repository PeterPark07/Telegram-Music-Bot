import os
from flask import Flask, request
import telebot
from helper.music import search, download_audio
from helper.log import send_log

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('music_bot'), threaded=False)
audio_format = 'm4a'  # Default value
state = False
admin_user = int(os.getenv('admin')) 
users = [int(id) for id in (os.getenv('users').split(','))]
last_message_id = None


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
    send_log(bot, message)
    # Handle the /start command
    bot.reply_to(message, "Hello there! I am MusicBot, your personal music assistant.\nTo find any song or audio, simply send me the title you want to search for.")


@bot.message_handler(commands=['help'])
def handle_help(message):
    # Handle the /help command
    bot.reply_to(message, "MusicBot Help:\n\nSend me the title or description of a song or audio you want to find, and I will fetch it for you.\nUse /settings to change the audio format (Default = m4a).")

@bot.message_handler(commands=['on'])
def handle_on(message):
    send_log(bot, message)
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

@bot.message_handler(commands=['settings'])
def settings(message):
    # Create an inline keyboard for audio format selection
    keyboard = telebot.types.InlineKeyboardMarkup()
    # Create inline keyboard buttons for each audio format
    formats = ['best', 'aac', 'm4a', 'mp3', 'opus', 'wav']
    buttons = [telebot.types.InlineKeyboardButton(format_name, callback_data=format_name) for format_name in formats]
    # Add buttons to the keyboard
    keyboard.add(*buttons)

    # Send a message with the inline keyboard
    bot.send_message(message.chat.id, "Select your desired audio format:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global audio_format
    audio_format = call.data
    bot.send_message(call.message.chat.id, f"Audio format set to {call.data}")


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    send_log(bot, message)
    if not state and message.chat.id != admin_user and message.chat.id not in users :
        return

    global last_message_id 
  
    # Check if this is the same message as the previous one 
    if last_message_id == message.message_id: 
        return 
        
    # Store the current message ID as the most recent one 
    last_message_id = message.message_id

    query = message.text
    title, url, duration, duration_text= search(query)

    if not url:
        # No URL found, reply with the title
        bot.reply_to(message, title)
        return
    else:
        # Download audio file
        wait = bot.reply_to(message, f"{title}\n{duration}")
        return
        response, audio_file, thumbnail = download_audio(url, audio_format)
        bot.delete_message(message.chat.id, wait.message_id)

        if not audio_file:
            # Error downloading audio file
            bot.reply_to(message, response)
            return
        else:
            try:
                # Send photo with caption
                bot.send_photo(message.chat.id, thumbnail, caption=f"{title}\n\n{duration_text}\n\n{url}",reply_to_message_id=message.message_id)
            except:
                # Send message with caption
                bot.reply_to(message, f"{title}\n\n{duration_text}\n\n{url}")

            # Send audio file
            with open(audio_file, 'rb') as f:
                bot.send_audio(message.chat.id, f,title=title)
