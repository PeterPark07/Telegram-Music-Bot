import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch
import os

ytdl_opts = {'format': 'bestaudio/best',
             'postprocessors': [{'key': 'FFmpegExtractAudio',
                                 'preferredcodec': 'm4a',
                                 'preferredquality': 'best'}]}

def search(query):
  search = VideosSearch(query, limit=1)
  results = search.result().get('result')
  if not results:
      return "No videos found for that query." , None
  
  selected_video = results[0]
  url = f"https://www.youtube.com/watch?v={selected_video['id']}"
  return f"{selected_video['title']}..." , url

def download_audio(url):
  try:
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = info['requested_downloads'][0]['filepath']
        file_size = os.path.getsize(filepath)
        if file_size > 49 * 1024 * 1024:
            os.remove(filepath)
            return 'File larger than 50 MB.', None, None
        return None , filepath , None
  except:
    return 'Could not download file', None, None
