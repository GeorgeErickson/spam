from mrjob.job import MRJob
from itertools import tee
import chunker
import logging
import argparse

class TrainWordFreq(MRJob):
    """
    Generates a list of token, count pairs as tsv.
    Done as a map reduce job so that its crazy fast.
    """
    def emit_tokens(self, _, line):
        return chunker.chunk_by_word(line)
    
    def sum_tokens(self, token, counts):
        yield token, sum(counts)
    
    def group_tokens(self, token, token_sum):
        if token_sum > 5:
            yield None, (token, token_sum)
    
    def prob_tokens(self, _, token_counts):
        #must split the iterable, because it will get used up
        token_counts_1, token_counts_2 = tee(token_counts)
        
        #find the total number of words
        total = reduce(lambda i, tup: i+tup[1], token_counts_1, 0)
        
        #compute the probability
        for token, count in token_counts_2:
            yield token, (count / float(total))
            
    def steps(self):
        return [
            self.mr(
                mapper=self.emit_tokens,
                reducer=self.sum_tokens
            ), self.mr(
                mapper=self.group_tokens,
                reducer=self.prob_tokens
            )]
    
def run_job(infile, namespace):
    mr_job = TrainWordFreq(args=[infile,])
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            print key



parser = argparse.ArgumentParser(description='Load tsv output from train.py into a persistant store')
parser.add_argument('--ham', type=argparse.FileType('r'))
parser.add_argument('--spam', type=argparse.FileType('r'))
args = parser.parse_args()
if args.spam:
   run_job(args.spam, namespace='spam')
if args.ham:
    run_job(args.ham, namespace='ham')