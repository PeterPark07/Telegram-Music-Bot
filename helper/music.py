import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch

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
    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info['formats']
        audio_formats = [f for f in formats if f.get('vcodec') == 'none']
        download_url = audio_formats[-2].get('url')
        extension = audio_formats[-2].get('ext')
        video_title = info.get('title')
        video_title_with_extension = f"{video_title}.{extension}"
        return None , download_url , video_title_with_extension 
  except:
    return 'Could not download file', None, None
