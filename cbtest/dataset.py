# utils for CBT dataset.
import re
import pickle
from pprint import pprint
from cbtest.config import cbt_cn_test

def read_cbt(path, limit=None):
    '''
    read in a children's book dataset.
    return list of dicts. Each dict is an object with keys:
        1. context   # the context sentences.
        2. query     # the query with blank.
        3. answer    # correct answer word.
        4. candidate # list of answer candidates
    '''
    with open(path, 'r') as f:
        exs = []
        context = []
        for line in f:
            line = line.replace('\n', '')

            # empty?
            if line == '':
                continue

            # process 
            m = re.match(r'[0-9]* ', line).end() # get the index of line number, r'' means raw string
            line_no = int(line[:m-1]) #  the line number
            sentence = line[m:] # the sentence

            # if it is query.
            if line_no == 21: 
                sentence = sentence.split('\t') # the ans ,query and cand are seperated by a tab
                query = sentence[0].strip().split(' ')
                answer = sentence[1].strip()
                candidate = sentence[3].strip().split('|')
                candidate = [c for c in candidate if c] # now candidate is a list of all cand words

                while len(candidate) < 10:
                    candidate.append('<null>')
                assert(len(candidate) == 10)

                # ex is a dict
                ex = {
                    'context': context,
                    'query': query,
                    'answer': answer,
                    'candidate': candidate
                }
                assert(len(context) == 20)

                # append to a list of dicts -> exs
                exs.append(ex)

                # if we only want to train small amount, --small provided in arg
                if limit and len(exs) > limit:
                    break
                context = []

            # if it is normal sentence, append to context, it will be add to exs after we meet a query
            else:
                context.append(sentence.strip().split(' '))

        return exs


def copy_cbt(exs):
    '''
    make a deep copy of cbt dataset
    '''
    return pickle.loads(pickle.dumps(exs))


def lower(words):
    return [word.strip().lower() for word in words]


def filter(words, vocab):
    return [word for word in words if word in vocab]


def unkify(words, vocab, unk='<unk>'):
    return map(lambda word: word if word in vocab else unk, words)


def remove_punctuation(words):
    return [word for word in words if re.match(r'[a-zA-Z\-]+', word)] # TODO: avoid removing things like *bird's*

en_stopwords = None
def remove_stopwords(words):
    from nltk.corpus import stopwords
    global en_stopwords
    if not en_stopwords:
        en_stopwords = set(stopwords.words('english'))
    return [word for word in words if word not in en_stopwords]


