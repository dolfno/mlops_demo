from python_ci_template import console
import os
import pickle
import logging

log = logging.getLogger()
log.setLevel("DEBUG")


class TestException(Exception):
    pass


class FakeDataLoader:
    """Test helper class to cache data to be used in a test as a fixture

    Args:
        cache_filename: The filename (pkl) to store the cache
        fetch_data_method: The method to be mocked. Result of this method is stored in cache_filename
        **args: the arguments provided to the fetch_data_method
    """

    def __init__(self, cache_filename, fetch_data_method, **args) -> None:
        self.cache_filename = cache_filename
        self.fetch_data_method = fetch_data_method
        self.fetch_data_args = args

    def create_cache(self):
        log.debug("Create Cache")
        if os.path.isfile(self.cache_filename):
            self.clear()

        result = self.fetch_data_method(**self.fetch_data_args)

        with open(self.cache_filename, 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return True

    def clear(self):
        log.debug("Clearing Cache")
        if os.path.isfile(self.cache_filename):
            os.remove(self.cache_filename)
        else:
            log.info("Didn't find cache, so nothing to clear")

    @property
    def cache_exists(self) -> bool:
        return os.path.exists(self.cache_filename)

    def load_cache(self):
        log.debug("Loading Cache")
        with open(self.cache_filename, 'rb') as handle:
            results = pickle.load(handle)
        return results

    @property
    def data(self):
        log.debug("Fetching data")
        if not self.cache_exists:
            try:
                self.create_cache()
            except Exception:
                raise TestException(
                    "Cache not found and couldnt be created. Create fixtures locally first")
        results = self.load_cache()
        return results


def test_dataloader_data():
    f = FakeDataLoader("./fixtures/cassette.pkl", console.get_tags,
                       **{"glue_connection": "nldevun_a17a_ro"})
    assert f.data.iloc[0, 0] == 'ciqSQaQhmoiKB7ccPjXXrU'


def test_dataloader_create_cache():
    f = FakeDataLoader("./fixtures/cassette.pkl", console.get_tags,
                       **{"glue_connection": "nldevun_a17a_ro"})
    f.clear()
    assert f.create_cache() is True
