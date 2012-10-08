import os, sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), '..', 'stores'))
STORE_NAME = 'KeyValueStore'

def get_modules_to_test():
    """
    Searches for all modules that match *_store in this dir. These files are automatically tested
    """
    return [__import__(f[:-3]) for f in os.listdir(dirname(__file__)) if f.endswith('_store.py') and f != '__init__.py']

    
def test_stores_match_convention():
    """
    All modules that end with _store.py, should contain a module named STORE_NAME
    """
    for module in get_modules_to_test():
        assert hasattr(module, STORE_NAME)

def test_stores_get_set():
    """
    Get should return the key if it is there, default otherwise
    """
    for module in get_modules_to_test():
        store = module.KeyValueStore()
        
        #basic set/get
        store.set('test', 1)
        assert store.get('test') == 1

        #get no default
        assert store.get('test1') == None
        
        #get with default
        assert store.get('test2', 1) == 1
        
        #namespace
        store.set('test', 1, 'spam')
        store.set('test', 2, 'ham')
        assert store.get('test', namespace='spam') == 1
        assert store.get('test', namespace='ham') == 2
        
        store.close()