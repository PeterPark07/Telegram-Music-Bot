start = "Hello there! I am MusicBot, your personal music assistant.\n To find any song or audio, simply send me the title you want to search for."
help = "MusicBot Help: \n\nSend me the title or description of a song or audio you want to find, and I will fetch it for you."
on = "BOT ON"
off = "BOT OFF"

def commands(text , state):
    if text == '/start':
        return start 
    if text == '/help':
        return help 
    if text == '/on':
        state = True
        return on
    if text == '/off':
        state = False
        return 0
    else:
        return 0

def resolve(json):
    return json['message']['from']['id'] , json['message']['text']
