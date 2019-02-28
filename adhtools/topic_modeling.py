import click
from sklearn.feature_extraction.text import CountVectorizer
import adhtools.utils
import pandas as pd
import os
import numpy as np
"""Perform topic modeling with LDA on SAFAR stemmed XML files
  
The result is three files: a model.pkl file, a csv file with most important words per topic and a csv file with the topic distribution per document.
The model.pkl can be loaded and applied on unseen documents.
"""
import lda
import glob
import pickle

def train_model(corpus, external_stopwords, nr_topics, n_iter):
    vectorizer = CountVectorizer( stop_words=external_stopwords, min_df=2, max_df=0.9)
    X = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    model = lda.LDA(n_topics=nr_topics, n_iter=n_iter, random_state=1)
    model.fit(X)
    return model, feature_names

def get_corpus(book_files, input_type):
    """
    Create text corpus based on input format
    """
    if input_type=='stemmer':
        corpus = adhtools.utils.corpus_str(book_files, analyzer=False, field='proposed_root')
    elif input_type=='analyzer':
        corpus = adhtools.utils.corpus_str(book_files, analyzer=True, field='proposed_root')
    else:
        raise ValueError("Invalid value for input_type")
    return corpus

@click.command()
@click.argument('in_dir', type=click.Path())
@click.option('--stop_words', default=None, type=click.File(encoding='utf-8'))
@click.option('--nr_topics', '-n', default=10, type=int)
@click.option('--n_iter', '-i', default=500, type=int)
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
@click.option('--input_type', type=click.Choice(['analyzer', 'stemmer']), default='stemmer')
def topic_modeling(in_dir, stop_words, nr_topics, n_iter, out_dir, input_type):
    # Create corpus based on input XML files
    book_files = glob.glob(os.path.join(in_dir, '*.xml'))
    fnames = [os.path.basename(fn) for fn in book_files]
    external_stopwords = [line.strip() for line in stop_words] if stop_words is not None else []
    analyzer = input_type == 'analyzer'
    corpus = get_corpus(book_files, input_type)
    
    model, feature_names = train_model(corpus, external_stopwords, nr_topics, n_iter)

    # Retrieve topic distribution for documents
    df_document_topics = pd.DataFrame(model.doc_topic_, index=fnames)
    df_document_topics.to_csv(os.path.join(out_dir, 'document_topics_{}.csv'.format(nr_topics)))
    
    # Retrieve most important 10 words per topic
    topic_words = pd.DataFrame(np.argsort(model.components_, axis=1)[:,-10:][::-1])
    topic_words = topic_words.applymap(lambda l: feature_names[l])
    topic_words.to_csv(os.path.join(out_dir, 'topics_{}.csv'.format(nr_topics)))
    
    # Save the model object. The trained model can be applied to unseen documents.
    with open(os.path.join(out_dir, 'model_{}.pkl'.format(nr_topics)), 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    topic_modeling()