import redis
import re
class KeyValueStore():
    """
    Simple Storage backend that stores all of the data using Redis.
    """
    delimiter = '|:::|'
    def __init__(self, port=6379, db=0):
        self._store = redis.StrictRedis(host='localhost', port=port, db=db)
    
    def add_namespace(self, key, namespace):
        return "%s%s%s" % (namespace, self.delimiter, re.sub(r'\W+', '', key))
    def get(self, key, default=None, namespace=None):
        """
        Return the value at key, return None otherwise.
        """
        if namespace:
            key = self.add_namespace(key, namespace)
        
        value = self._store.get(key)
        if default != None and value is None:
            value = default
        return value
    
    def set(self, key, val, namespace=None):
        if namespace:
            key = self.add_namespace(key, namespace)
        self._store[key] = val
    
    def close(self):
        self._store.close()