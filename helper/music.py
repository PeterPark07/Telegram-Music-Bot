import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch
import os

ytdl_opts = {'format': 'bestaudio/best',
             'postprocessors': [{'key': 'FFmpegExtractAudio',
                                 'preferredcodec': 'best',
                                 'preferredquality': 'best'}]}

def search(query):
  search = VideosSearch(query, limit=1)
  results = search.result().get('result')
  if not results:
      return "No videos found for that query." , None
  
  selected_video = results[0]
  print(selected_video)
  url = selected_video['link']
  title = selected_video['title']
  duration = selected_video['duration']
  thumbnail = selected_video['thumbnails'][0]['url']
  return title , url , duration , thumbnail

def download_audio(url):
  try:
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = info['requested_downloads'][0]['filepath']
        file_size = os.path.getsize(filepath)
        if file_size > 49 * 1024 * 1024:
            os.remove(filepath)
            return 'File larger than 50 MB.', None
        return None , filepath 
  except:
    return 'Could not download file', None
