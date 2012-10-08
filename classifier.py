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
    spam - 40.9149477958
    spam 2 - 41.9583589197 
    easy_ham - 21.6706759094
    hard_ham - 41.0932577021
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
                weight = is_spam(f.read(), store)
                avgg += weight
                print weight
                c += 1
        print "Average: %s" % str(avgg / c)
 