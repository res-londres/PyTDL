import yt_dlp

def download_mp3(url, dst='.'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{dst}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    # test: download american pie
    download_mp3('https://www.youtube.com/watch?v=PRpiBpDy7MQ')