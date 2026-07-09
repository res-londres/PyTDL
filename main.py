import argparse
from search_yt import SearchYT
from downloader import Downloader

def main():
    parser = argparse.ArgumentParser(description='PyTDL - YouTube to MP3 downloader')
    parser.add_argument(
        'input_file',
        help='Text file with lines of queries')
    parser.add_argument(
        '-d', '--destination',
        default='Downloads',
        help='Destination directory')
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        queries = [line.strip() for line in f if line.strip()]

    print('STARTING SEARCH...')
    results = SearchYT.search_yt_mult(queries)
    audio_metadata = [(info.get('title'), info.get('webpage_url')) for info in results]

    print('STARTING DOWNLOAD...')
    Downloader.download_mp3_mult(audio_metadata, dst=args.destination)

if __name__ == '__main__':
    main()