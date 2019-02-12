#!/usr/bin/env python
"""Extract Quran quotes from Safar XML files with header/quote information.
"""
import click
from lxml import etree
from tqdm import tqdm
import pandas as pd
import os
import glob

def extract_quotes(fname, quote_type = 'quran'):
    quotes = []
    context = etree.iterparse(fname, events=('end', ),tag=('word', 'quote'), encoding='utf-8')
    book_id = os.path.basename(fname)[:-4]
    for event, elem in context:
        if elem.tag == 'quote' and elem.attrib['type']==quote_type:
            refs = list(elem.getchildren())
            if len(refs)>0:
                ref_position = refs[0].attrib['id']
            else:
                ref_position = -1

            quotes.append({'BookURI': book_id,
                           'quote': elem.attrib['text'],
                          'position': ref_position})
        # make iteration over context fast and consume less memory
        # https://www.ibm.com/developerworks/xml/library/x-hiperfparse
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    return quotes



@click.command()
@click.argument('in_dir', type=click.Path())
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def extract_quotes_xml(in_dir, out_dir):
    """Extract Quran quotes from Safar XML files.

    Write the output to one csv file, containing the quote and position in the file.
    """
    book_files = glob.glob(os.path.join(in_dir,'*.xml'))
    print(len(book_files))
    quotes = []
    for fname in tqdm(book_files):
        quotes.extend(extract_quotes(fname))

    quotes_df = pd.DataFrame(quotes)
    quotes_df.to_csv(os.path.join(out_dir, 'quran_quotes.csv'), index=False, encoding='utf-8')

if __name__ == '__main__':
    extract_quotes_xml()
