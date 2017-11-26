import youtube_dl

class CachingClient:
    def __init__(self, client, cache):
        self.client = client
        self.cache = cache

    def get_video_data(self, id, subtitles=True):
        return self._get(lambda x: f'video:{x}', id, self.client.get_video_data)

    def get_playlist_data(self, id):
        return self._get(lambda x: f'playlist:{x}', id, self.client.get_playlist_data, self._cache_videos)

    def get_channel_data(self, id):
        return self._get(lambda x: f'channel:{x}', id, self.client.get_channel_data, sel._cache_videos)

    def _get(self, cache_key_gen_func, id, get_func, post_process_func):
        key = cache_key_gen_func(id)
        found, data = self.cache.get(key)
        if not found:
            data = get_func(id)
            self.cache.add(key, data)
            if post_process_func:
                post_process_func(data)(self.cache)
        return data

    def _cache_videos(self, playlist):
        assert playlist['_type'] == 'playlist'
        def wrapper(cache):
            for entry in playlist.get('entries'):
                cache.add(f"video:{entry['id']}", entry)
        return wrapper

    def stats(self):
        return self.cache.stats()

class Client:
    def __init__(self, client):
        self.client = client

    def get_video_data(self, id, subtitles=True):
        return self._get(f'https://www.youtube.com/watch?v={id}')

    def get_playlist_data(self, id):
        return self._get(f'https://www.youtube.com/playlist?list={id}')

    def get_channel_data(self, id):
        return self._get(f'https://www.youtube.com/channel/{id}')

    def _get(self, url):
        return self.client.extract_info(url, download=False)
