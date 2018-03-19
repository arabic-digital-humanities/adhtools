
# coding: utf-8
from lxml import etree
import pandas as pd
import sys
import os
import click

def transform_file(fn_in, fp_out, lemma):
    with open(fn_in) as f:
        safar_el = etree.parse(f)

    # Parse file into dataframe
    df = pd.DataFrame()
    for w in safar_el.iter('word'):
        word_id = w.attrib['w_id']
        word_value = w.attrib['value']
        a_dict = [a.attrib for a in w.iter('analysis')]
        w_df = pd.DataFrame.from_records([dict(a_list) for a_list in a_dict])
        w_df['w_id'] = word_id
        w_df['value'] = word_value
        df = df.append(w_df)
    if len(df)==0:
        raise Exception("File contains no words")
    df['w_id'] = df['w_id'].astype('int')

    # word, lemma, pos
    df_reduced = df.groupby('w_id').first()[['value', lemma, 'type']]
    df_reduced.columns = ['word', 'lemma', 'pos']
    df_reduced[df_reduced=='#'] = ''

    fn_out = os.path.join(fp_out, os.path.splitext(os.path.basename(fn_in))[0]+'.csv')
    df_reduced.to_csv(fn_out, index=False)

@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
@click.option('--lemma', default='root')
def main(in_file, out_dir, lemma):
    transform_file(in_file, out_dir, lemma)

if __name__ == "__main__":
    main()



