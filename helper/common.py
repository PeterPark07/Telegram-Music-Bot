start = "Hello there! I am MusicBot, your personal music assistant.\n To find any song or audio, simply send me the title you want to search for."
help = "MusicBot Help: \n\nSend me the title or description of a song or audio you want to find, and I will fetch it for you."
on = "BOT ON"
off = "BOT OFF"

def commands(text, state):
    if text == '/start':
        msg = start
    elif text == '/help':
        msg = help
    elif text == '/on':
        msg = on
        state = True
    elif text == '/off':
        msg = off
        state = False
    else:
        msg = 0
    return msg, state

def resolve(json):
    return json['message']['from']['id'] , json['message']['text']
