import argparse, sys
from stores.redis_store import KeyValueStore

def load(tsv_file, namespace, coefficient=1):
    store = KeyValueStore()
    for token, value in (line.split('\t') for line in tsv_file):
        store.set(token, float(value) * coefficient, namespace=namespace)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load tsv output from train.py into a persistant store')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--spam', action='store_true', default=False, dest='is_spam')
    args = parser.parse_args()
    if args.is_spam:
       load(args.infile, namespace='spam')
    if not args.is_spam:
        load(args.infile, namespace='ham', coefficient=2)
