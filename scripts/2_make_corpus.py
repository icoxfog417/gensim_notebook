# -*- coding: utf-8 -*-
import sys
import os
import argparse
from gensim import corpora
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

def parse(salon):
    text = salon["kodawari"]
    parsed = text.split("/")
    parsed = [p for p in parsed if p]
    return parsed

if __name__ == "__main__":
    # for command line tool
    parser = argparse.ArgumentParser(description="Make corpus from salons data file.")
    parser.add_argument("datafile", type=str, help="salon data file (json format).")
    parser.add_argument("--no_below", type=int, default=5, help="cut under the n count word.")
    parser.add_argument("--no_above", type=float, default=0.5, help="cut the words which appears above n% of documents (=very frequently word).")
    parser.add_argument("--keep_n", type=int, default=100000, help="keep n words.")
    args = parser.parse_args()

    encoding = "utf-8"
    path = args.datafile
    if not os.path.isfile(path):
        raise Exception("File is not found at {0}.".format(path))

    ignores_file = os.path.join(os.path.dirname(path), "ignores.txt")
    ignores = []
    with open(ignores_file, "r", encoding=encoding) as f:
        ignores = [line.replace(os.linesep, "") for line in f]

    # make dictionary
    salons = []
    dictionary = None
    with open(path, "r", encoding=encoding) as f:
        salons = json.load(f)
        dictionary = corpora.Dictionary(parse(s) for s in salons)

    # ref: https://radimrehurek.com/gensim/corpora/dictionary.html#gensim.corpora.dictionary.Dictionary.filter_extremes
    dictionary.filter_extremes(no_below=args.no_below, no_above=args.no_above, keep_n=args.keep_n)
    stop_ids = [dictionary.token2id[ig] for ig in ignores if ig in dictionary.token2id]
    dictionary.filter_tokens(stop_ids)
    dictionary.compactify()

    # make corpus
    corpus = [dictionary.doc2bow(parse(s)) for s in salons]

    # show words
    for k, v in sorted(dictionary.dfs.items(), key=lambda i: i[1], reverse=True):
        print("{0}: {1}".format(dictionary.get(k), v))

    # save dictionary
    corpus_file = os.path.join(os.path.dirname(path), "salons_corpus.mm")
    dict_file = os.path.join(os.path.dirname(path), "salons_dict.dict")
    corpora.MmCorpus.serialize(corpus_file, corpus)
    dictionary.save(dict_file)
