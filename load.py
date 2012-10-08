import argparse
from stores.redis_store import KeyValueStore

def load(tsv_file, namespace):
    store = KeyValueStore()
    for token, value in (line.split('\t') for line in tsv_file):
        store.set(token, float(value), namespace=namespace)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load tsv output from train.py into a persistant store')
    parser.add_argument('--ham', type=argparse.FileType('r'))
    parser.add_argument('--spam', type=argparse.FileType('r'))
    args = parser.parse_args()
    if args.spam:
       load(args.spam, namespace='spam')
    if args.ham:
        load(args.ham, namespace='ham')
