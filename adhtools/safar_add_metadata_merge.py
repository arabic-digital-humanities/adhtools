#!/usr/bin/env python
import click
import codecs
import os
import copy
from bs4 import BeautifulSoup
from nlppln.utils import out_file_name, get_files


@click.command()
@click.argument('in_dir', type=click.Path(exists=True))
@click.argument('in_dir_meta', type=click.Path(exists=True))
@click.argument('in_file_meta', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def safar_add_metadata(in_dir, in_dir_meta, in_file_meta, out_dir):
    in_files = get_files(in_dir)
    metadata_files = {os.path.basename(fn): fn for fn in get_files(in_dir_meta)}
    
    doc_id = os.path.splitext(os.path.basename(in_file_meta))[0]
        
    out_dir_sub = os.path.join(out_dir, doc_id)
    if not os.path.exists(out_dir_sub):
        os.mkdir(out_dir_sub)
    
    with open(in_file_meta) as fn:
        metadata_all = BeautifulSoup(fn, 'xml')
    
    for in_file in in_files:
        metadata_file = metadata_files[os.path.basename(in_file)]
        with open(metadata_file) as f:
            metadata = BeautifulSoup(f, 'xml')
        with codecs.open(in_file, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'xml')

        # Make document with a single root element
        document = BeautifulSoup('<document></document>', 'xml')
        md_all = copy.copy(metadata_all.metadata)
        md = copy.copy(metadata.metadata)
        # add common meta data
        for m in md_all.find_all('meta'):
            md.append(m)
        document.document.append(md)
        try:
            document.document.append(soup.morphology_analysis)
        except:
            document.document.append(soup.stemmer_analysis)
        xml_out = out_file_name(out_dir_sub, in_file)
        with codecs.open(xml_out, 'wb', encoding='utf-8') as f:
            f.write(document.prettify())


if __name__ == '__main__':
    safar_add_metadata()
