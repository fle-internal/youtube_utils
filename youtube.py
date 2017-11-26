import youtube_dl

class CachingClient:
    def __init__(self, client, cache):
        self.client = client
        self.cache = cache

    # TODO: Use the underlying client subtitle configuration as part of the composite caching key,
    # to do the caching very granular in regards to the kind of subtitle that the payload has
    def get_video_data(self, id, subtitles=True):
        return self._get(lambda x: f'video:{x}', id, self.client.get_video_data)

    def get_playlist_data(self, id):
        return self._get(lambda x: f'playlist:{x}', id, self.client.get_playlist_data, self._cache_videos)

    # TODO: Possible add a playlist caching item for the channel as well (since it seems that every channel is a playlist)
    def get_channel_data(self, id):
        return self._get(lambda x: f'channel:{x}', id, self.client.get_channel_data, self._cache_videos)

    def _get(self, cache_key_gen_func, id, get_func, post_process_func=None):
        key = cache_key_gen_func(id)
        found, data = self.cache.get(key)
        if not found:
            data = get_func(id)

            # TODO: If we had an `etag` to control the version of the payload retrieved,
            # it would give us better control to invalidate the cache
            self.cache.add(key, data)
            if post_process_func:
                post_process_func(data)(self.cache)
        return data

    def _cache_videos(self, playlist):
        assert playlist['_type'] == 'playlist'
        def wrapper(cache):
            for entry in playlist.get('entries'):
                cache.add(f"video:{entry['id']}", entry)

            # TODO: group by video's playlist_id and add those items
        return wrapper

    def stats(self):
        return self.cache.stats()

class Client:
    def __init__(self, client):
        self.client = client

    # TODO: what's the correct video URL to use?
    def get_video_data(self, id, subtitles=True):
        return self._get(f'https://www.youtube.com/watch?v={id}')

    def get_playlist_data(self, id):
        return self._get(f'https://www.youtube.com/playlist?list={id}')

    def get_channel_data(self, id):
        return self._get(f'https://www.youtube.com/channel/{id}')

    def _get(self, url):
        return self.client.extract_info(url, download=False)
