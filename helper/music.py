import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch
import os

ytdl_opts = {'format': 'bestaudio/best',
             'postprocessors': [{'key': 'FFmpegExtractAudio',
                                 'preferredcodec': 'mp3',
                                 'preferredquality': 'best'}]}

def search(query):
  search = VideosSearch(query, limit=1)
  results = search.result().get('result')
  if not results:
      return "No videos found for that query." , None
  
  selected_video = results[0]
  url = f"https://www.youtube.com/watch?v={selected_video['id']}"
  return f"{selected_video['title']}..." , url

def download(url):
  try:
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = info['requested_downloads'][0]['filepath']
        file_size = os.path.getsize(filepath)
        if file_size > 50 * 1024 * 1024:
            response = "File larger than 50 MB."
            os.remove(filepath)
            return response , None
        return None , filepath
  except:
    return 'Could not download file' , None
  
def delete(path):
  os.remove(path)
