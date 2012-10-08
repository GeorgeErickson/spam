import shelve
from os.path import dirname, join

SHELF_DATA_PATH = join(dirname(__file__), '..', 'data', 'shelve.data')


class KeyValueStore():
    """
    Simple Storage backend that stores all of the data using shelve.
    """
    delimiter = '|:::|'
    def __init__(self):
        self._store = shelve.open(SHELF_DATA_PATH)
    
    def add_namespace(self, key, namespace):
        return "%s%s%s" % (namespace, self.delimiter, key)
    
    def get(self, key, default=None, namespace=None):
        """
        Return the value at key, return None otherwise.
        """
        if namespace:
            key = self.add_namespace(key, namespace)
        
        if self._store.has_key(key):
            return self._store[key]
        else:
            return default
    
    def set(self, key, val, namespace=None):
        if namespace:
            key = self.add_namespace(key, namespace)
        self._store[key] = val
    
    def close(self):
        self._store.close()

