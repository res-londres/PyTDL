import argparse
from pathlib import Path

from downloader import Downloader
from search_yt import SearchYT

parser = argparse.ArgumentParser(description='Download audio from YouTube')
parser.add_argument('input_file', help='Text file with lines of queries')
parser.add_argument('-d', '--destination', default='Downloads', help='Destination directory')

args = parser.parse_args()

class PyTDL:
    def __init__(self):
        self.queries = list()
        self.audio_metadata = list()
        self._successful_downloads = 0
        self._failed_downloads = 0

    def run(self, input_file, destination='Downloads'):
        try:
            self.add_queries(input_file)
        except FileNotFoundError:
            print(f'File not found: {input_file}')
            return
        self.search()
        while True:
            self.download(destination)
            self.check_download_failures(destination)
            if self.audio_metadata:
                self._failed_downloads = len(self.audio_metadata)
                retry = input(f'{self._failed_downloads} downloads failed. Retry download? (y/n) ')
                if retry.lower() == 'n':
                    break
            break
        self._successful_downloads -= self._failed_downloads
        print(f'Download complete. {self._successful_downloads} successful downloads, {self._failed_downloads} failed downloads.')
        
    def add_queries(self, input_file):
        with open(input_file, 'r') as f:
            self.queries = [line.strip() for line in f if line.strip()]

    def search(self):
        print('STARTING SEARCH...')
        results = SearchYT.search_yt_mult(self.queries)
        self.audio_metadata = [(info.get('title'), info.get('webpage_url')) for info in results]
        # assume everything succeeds first, subtract failed downloads later
        self._successful_downloads = len(self.audio_metadata)

    def download(self, destination='Downloads'):
        print('STARTING DOWNLOAD...')
        Downloader.download_mp3_mult(self.audio_metadata, dst=destination)

    def check_download_failures(self, destination='Downloads'):
        downloaded_titles = {p.stem for p in Path(destination).glob('*.mp3')}
        # audio metadata of titles that failed to download
        self.audio_metadata = [(title, url) for title, url in self.audio_metadata if title not in downloaded_titles]

if __name__ == '__main__':
    pydtl = PyTDL()
    pydtl.run(args.input_file, args.destination)
