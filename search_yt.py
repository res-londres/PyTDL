from concurrent.futures import ThreadPoolExecutor
import itertools
import yt_dlp

class SearchYT:
    @staticmethod
    def search_yt(query, quiet=False):
        # returns info of top yt search result
        ydl_opts = {
            'default_search': 'ytsearch1:',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(query, download=False)
            except:
                if not quiet:
                    print(f'No results for query "{query}"')
                return dict()
            if not quiet:
                print(f'Found results for query "{query}"')
            top_result = result['entries'][0]
            return top_result

    @staticmethod
    def search_yt_mult(queries, quiet=False):
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(
                SearchYT.search_yt, queries,
                itertools.repeat(quiet)
            )
        return list(result for result in results if result)

if __name__ == '__main__':
    # test
    with open('test', 'r') as f:
        queries = [line.strip() for line in f if line.strip()]
    search_yt = SearchYT
    audio_metadata = search_yt.search_yt_mult(queries)



