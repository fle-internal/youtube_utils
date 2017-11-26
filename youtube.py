import youtube_dl

class CachingClient:
    def __init__(self, client, cache):
        self.client = client
        self.cache = cache

    def get_video_data(self, id, subtitles=True):
        return self._get(lambda x: f'video:{x}', id, self.client.get_video_data)

    def get_playlist_data(self, id):
        return self._get(lambda x: f'playlist:{x}', id, self.client.get_playlist_data)

    def get_channel_data(self, id):
        return self._get(lambda x: f'channel:{x}', id, self.client.get_channel_data)

    def _get(self, cache_key_gen_func, id, get_func):
        key = cache_key_gen_func(id)
        found, data = self.cache.get(key)
        if not found:
            data = get_func(id)
            self.cache.add(key, data)
        return data

    def stats(self):
        return self.cache.stats()

class Client:
    def __init__(self, client):
        self.client = client

    def get_video_data(self, id, subtitles=True):
        raise Exception('Not Implemented')

    def get_playlist_data(self, id):
        raise Exception('Not Implemented')

    def get_channel_data(self, id):
        return self._get(lambda x: f'https://www.youtube.com/channel/{x}', id)

    def _get(self, gen_url, id):
        url = gen_url(id)
        return self.client.extract_info(url, download=False)
