#!/usr/bin/env python
import click
import codecs
import os
import copy
from bs4 import BeautifulSoup
from nlppln.utils import out_file_name, get_files


@click.command()
@click.argument('in_dir', type=click.Path(exists=True))
@click.argument('metadata', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def safar_add_metadata(in_dir, metadata, out_dir):
    in_files = get_files(in_dir)
    
    out_dir_sub = os.path.join(out_dir, 'output')
    if not os.path.exists(out_dir_sub):
        os.mkdir(out_dir_sub)
        
    metadata = BeautifulSoup(metadata, 'xml')
    
    for in_file in in_files:
        with codecs.open(in_file, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'xml')

        md = copy.copy(metadata)
        soup.insert(0, md.metadata)

        xml_out = out_file_name(out_dir_sub, in_file)
        with codecs.open(xml_out, 'wb', encoding='utf-8') as f:
            f.write(soup.prettify())


if __name__ == '__main__':
    safar_add_metadata()
