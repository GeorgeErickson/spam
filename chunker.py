import re
WORD_RE = re.compile(r"[\w']+")

def chunk_by_word(in_string):
    for word in WORD_RE.findall(in_string):
        yield (word.lower(), 1)
    
    