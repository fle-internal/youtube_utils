import unittest

import os

from cache import Db
from tempfile import mkdtemp
from youtube import Client, CachingClient
import youtube_dl


class TestCachingClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_dir = os.getcwd()
        dirname = os.path.join(current_dir, '.cache', 'cachingclienttests')
        os.makedirs(dirname, exist_ok=True)
        print(dirname)
        cls.cache = Db(dirname, 'youtube').__enter__()
        cls.ytd = Client(youtube_dl.YoutubeDL(dict(
            verbose=True,
        )))

    @classmethod
    def teadDownClass(cls):
        cls.cache.__exit__()
        cls.ytd.__exit__()

    def setUp(self):
        self.caching_client = CachingClient(TestCachingClient.ytd, TestCachingClient.cache)

    def tearDown(self):
        self.caching_client = None

    def test_get_channel_data(self):
        data = self.caching_client.get_channel_data('UCwYh0qBAF8HyKt0KUMp1rNg')
        self.assertIsNotNone(data)

    def test_get_channel_data_twice(self):
        data = self.caching_client.get_channel_data('UCwYh0qBAF8HyKt0KUMp1rNg')
        self.assertIsNotNone(data)
        data = self.caching_client.get_channel_data('UCwYh0qBAF8HyKt0KUMp1rNg')
        self.assertIsNotNone(data)
        stats = self.caching_client.stats()
        self.assertGreaterEqual(stats['hits'], 2)

if __name__ == '__main__':
    unittest.main()
