from stores.redis_store import KeyValueStore
import chunker, os, argparse, sys

def token_weight(word, store):
    prob_in_spam = float(store.get(word, default=0, namespace='spam'))
    prob_not_spam = float(store.get(word, default=0, namespace='ham'))
    
    #conditional probability of a word given the mail is spam
    if prob_in_spam + prob_not_spam > 0:
        cps = prob_in_spam / (prob_in_spam + prob_not_spam)
    
        #conditional probability of a word given the mail is legitimate
        cpns = prob_not_spam / (prob_in_spam + prob_not_spam)
        if cpns == 0:
            return 0
        return cps / cpns
    return 0

def is_spam(msg_string, store):
    """
    Avg weights:
    spam - ?
    spam 2 - ? 
    easy_ham - ?
    hard_ham - ?
    """
    
    avg = 0
    for total, word in enumerate(chunker.chunk_by_word(msg_string)):
        avg += token_weight(word[0], store)
    return (avg / total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate average weights')
    parser.add_argument('--dir', dest='dir', type=str)
    args = parser.parse_args()
    if args.dir:
        store = KeyValueStore()
        avgg = 0
        c = 0.0
        for infile in os.listdir(args.dir):
            with open(os.path.join(args.dir,infile)) as f:
                avgg += is_spam(f.read(), store)
                c += 1
        print avgg / c
 