#!/usr/bin/env python
import click
import codecs
import os
import re
import nltk

from Bio import pairwise2

from nlppln.utils import create_dirs, out_file_name


def tokenize(text):
    tokens = nltk.word_tokenize(text)

    # nltk tokenizer replaces " (double quotes) with `` and ''.
    # We want to keep the double quotes, so replace them again.
    tokens = ['"' if t == '``' or t == "''" else t for t in tokens]

    return tokens


def get_spaces_pattern(text):
    # replace regular expressions special characters
    for p in ('(', ')'):
            text = text.replace(p, '#')
    tokens = tokenize(text)
    m = re.match(r'( *)'.join(tokens), text)
    return m.groups()


def merge_sentences(l1, l2, check_duplicates=True):
    if check_duplicates and l1 == l2:
        print 'same!'
        return l1

    merged = []

    print 'sentence'
    idx1 = 0
    idx2 = 0

    print type(l1)
    print type(l2)

    #print len(l1), len(l2)
    # normalize spaces
    l1 = re.sub(r' +', u' ', l1)
    l2 = re.sub(r' +', u' ', l2)

    # remove trailing whitespace
    l1 = l1.strip()
    l2 = l2.strip()

    #print len(l1), len(l2)

    tokens1 = tokenize(l1)
    tokens2 = tokenize(l2)

    print len(tokens1), len(tokens2)

    print 'l1 is printable: ', all(c in string.printable for c in l1)
    print 'l2 is printable: ', all(c in string.printable for c in l2)

    # get spaces patterns
    try:
        text = l1
        spaces1 = get_spaces_pattern(text)
    except:
        print 'Spaces1 error'
        print l1
        print u'#'.join(tokens1)
        print text

    try:
        text = l2
        spaces2 = get_spaces_pattern(text)
    except:
        print 'Spaces2 error'

    print len(spaces1), len(spaces2)
    print '---'

    alignment = pairwise2.align.localms(tokens1,tokens2,2,-1,-0.5,-0.1, gap_char=["GAP"])
    #print alignment
    #print len(alignment)
    for t1, t2 in zip(alignment[0][0], alignment[0][1]):
        print t1, t2
        if t1 == t2:
            #print 'equal'
            #print_char(1, idx1+1, l1[idx1+1])
            merged.append(t1)
            try:
                merged.append(spaces1[idx1])
                if spaces1[idx1] == u' ':
                    print 'adding space based on l1'
            except IndexError:
                # no space to be added
                pass
            idx1 += 1
            idx2 += 1

        elif t1 == 'GAP':
            merged.append(t2)
            try:
                merged.append(spaces2[idx2])
                if spaces2[idx2] == ' ':
                    print 'adding space based on l2'
            except IndexError:
                pass
            idx2 += 1

        elif t2 == 'GAP':
            merged.append(t1)

            try:
                merged.append(spaces1[idx1])

                if spaces1[idx1] == u' ':
                    print 'adding space based on l1'
            except IndexError:
                pass
            idx1 += 1
        else:
            print 'Problem!'
    merged.append('\n')
    return ''.join(merged)


@click.command()
@click.argument('in_file1', type=click.File(encoding='utf-8'))
@click.argument('in_file2', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def merge2openiti(in_file1, in_file2, out_dir):
    create_dirs(out_dir)

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    lines1 = in_file1.readlines()
    lines2 = in_file2.readlines()

    merged = []
    for l1, l2 in zip(lines1[:10], lines2[:10]):
        merged_sentence = merge_sentences(l1, l2)
        merged.append(merged_sentence)

    out_file = out_file_name(out_dir, in_file1.name)
    print out_file
    with codecs.open(out_file, 'wb', encoding='utf-8') as f:
        f.write(''.join(merged))


if __name__ == '__main__':
    merge2openiti()
