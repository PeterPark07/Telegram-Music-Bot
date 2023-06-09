import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch

def search(query):
    # Perform a search for videos based on the query
    search = VideosSearch(query, limit=1)
    results = search.result().get('result')
    if not results:
        return "No videos found for that query.", None, None

    selected_video = results[0]
    # Check if the selected video has a duration , filter for live videos
    if selected_video['duration'] is None:
        return "Give a more relevant query.", None, None

    url = selected_video['link']
    title = selected_video['title']
    duration = selected_video['duration']
    duration_text = selected_video['accessibility']['duration']

    duration = duration.split(':')
    if len(duration) == 2:
        seconds = int(duration[0]) * 60 + int(duration[1])
    elif len(duration) == 3:
        seconds = int(duration[0]) * 3600 + int(duration[1]) * 60 + int(duration[2])
    else:
        seconds = int(duration[0])

    return title, url, seconds, duration_text

def download_audio(url , codec):
    # YouTube DL options for audio extraction
    ytdl_opts = {
        'format': 'bestaudio/best',
        "embed_metadata": True,
        "geo_bypass": True,
        "quiet": True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': 'best'
        }]
    }
    
    try:
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = info['requested_downloads'][0]
            thumbnail = [i['url'] for i in info['thumbnails'] if i['url'].endswith('.jpg')][-1]

            if file['filesize'] > 49 * 1024 * 1024:
                return 'File larger than 50 MB.', None , None
            
            return None, file['filepath'] , thumbnail
    except:
        return 'Could not download file', None , None
