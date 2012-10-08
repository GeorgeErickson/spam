from stores.redis_store import KeyValueStore
import chunker, os

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
    spam - 42.0348596581
    easy_ham - 24.4390063052
    hard_ham - 40.5205994778
    """
    
    avg = 0
    for total, word in enumerate(chunker.chunk_by_word(msg_string)):
        avg += token_weight(word[0], store)
    return (avg / total)


 
path = '/Users/gerickson/Desktop/spam/'
store = KeyValueStore()
avgg = 0
c = 0.0
for infile in os.listdir(path):
    with open(os.path.join(path,infile)) as f:
        avgg += is_spam(f.read(), store)
        c += 1
print avgg / c