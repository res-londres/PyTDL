from concurrent.futures import ThreadPoolExecutor
import itertools
import yt_dlp

class Downloader:
    @staticmethod
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

    @staticmethod
    def download_mp3s(urls, dst='.'):
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(Downloader.download_mp3, urls, itertools.repeat(dst))

if __name__ == '__main__':
    # test
    dl = Downloader()
    dl.download_mp3s(
        [
            'https://www.youtube.com/watch?v=HSSWn3wiRlM',
            'https://www.youtube.com/watch?v=PRpiBpDy7MQ',
            'https://www.youtube.com/watch?v=flF5aU1iZFo',
        ]
    )

