import itertools
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import yt_dlp # type: ignore

class Downloader:
    @staticmethod
    def download_mp3(audio_metadata, dst='.', quiet=False):
        title, url = audio_metadata

        if getattr(sys, 'frozen', False):
            ffmpeg_path = os.path.join(getattr(sys, '_MEIPASS', '.'), 'ffmpeg')
        else:
            ffmpeg_path = '/usr/bin/ffmpeg'  

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{dst}/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            if not quiet:
                print(f'Downloading: {title}...')
            ydl.download([url])

    @staticmethod
    def download_mp3_mult(audio_metadata, dst='.', quiet=False):
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(
                Downloader.download_mp3, audio_metadata,
                itertools.repeat(dst),
                itertools.repeat(quiet)
            )

if __name__ == '__main__':
    # test
    dl = Downloader()
    dl.download_mp3_mult(
        [
            ('X', 'https://www.youtube.com/watch?v=HSSWn3wiRlM'),
            ('Y', 'https://www.youtube.com/watch?v=PRpiBpDy7MQ'),
            ('Z', 'https://www.youtube.com/watch?v=flF5aU1iZFo'),
        ],
    )

