import yt_dlp

def search_yt(query):
    # returns info of top yt search result
    ydl_opts = {
        'default_search': 'ytsearch1:',
        'noplaylist': True,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        top_result = result['entries'][0]
        return top_result

if __name__ == '__main__':
    # test
    query = input('search for video: ')
    result = search_yt(query)
    print(result.get('webpage_url'))



