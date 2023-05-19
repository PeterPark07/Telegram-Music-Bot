start = "Hello there! I am MusicBot, your personal music assistant.\n To find any song or audio, simply send me the title you want to search for."
help = "MusicBot Help: \n\nSend me the title or description of a song or audio you want to find, and I will fetch it for you."
on = "BOT ON"
off = "BOT OFF"

def commands(text):
    if text == '/start':
        return start 
    if text == '/help':
        return help 
    if text == '/on':
        return on 
    if text == '/off':
        return off
    else:
        return 0
