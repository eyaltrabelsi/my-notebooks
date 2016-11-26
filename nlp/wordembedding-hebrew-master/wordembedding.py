#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import os
import os.path
import subprocess

import fasttext
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from tqdm import tqdm


def create_corpus(corpus_file="hewiki-latest-pages-articles.xml.bz2", output_="wiki.he.text"):
    if os.path.isfile(output_):
        print("corpus file {} already exists".format(output_))
        return

    if not os.path.isfile(corpus_file):
        print("Downloading wiki corpus")
        subprocess.call("wget https://dumps.wikimedia.org/hewiki/latest/{}".format(corpus_file), shell=True)

    print("Starting saving wiki articles to file")
    wiki = WikiCorpus(corpus_file, lemmatize=False, dictionary={})
    with open(output_, 'w') as output:
        for text in tqdm(wiki.get_texts()):
            article = " ".join([t.decode("utf-8") for t in text])
            output.write("{}\n".format(article.encode("utf-8")))


def get_word2vec_model(inp="wiki.he.text", out_model="wiki.he.word2vec.model"):
    if not os.path.isfile(out_model):
        print("Training Word2vec")
        model = Word2Vec(LineSentence(inp), sg=1,  # 0=CBOW , 1= SkipGram
                         size=100, window=5, min_count=5, workers=multiprocessing.cpu_count())
        model.init_sims(replace=True)  # trim unneeded model memory = use (much) less RAM
        model.save(out_model)

    return Word2Vec.load(out_model)


def get_fasttxt_model(inp="wiki.he.text", out_model="wiki.he.fasttext.model", alg="CBOW"):
    if not os.path.isfile('{}.bin'.format(out_model)):
        print("Training Fasttext")
        model = fasttext.skipgram(inp, out_model) if alg == "skipgram" else fasttext.cbow(inp, out_model)
        model.save(out_model)

    return fasttext.load_model('{}.bin'.format(out_model))


if __name__ == "__main__":
    pass
