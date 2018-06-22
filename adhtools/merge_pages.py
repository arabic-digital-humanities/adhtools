#!/usr/bin/env python
import click
import codecs
import os
import copy
from bs4 import BeautifulSoup
from nlppln.utils import out_file_name, get_files


@click.command()
@click.argument('in_dir', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def safar_add_metadata(in_dir, out_dir):
    in_files = get_files(in_dir)
    
    document = BeautifulSoup('<morphology_analysis></morphology_analysis>', 'xml')
    
    for in_file in in_files:
        with codecs.open(in_file, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'xml')
        morph_an = soup.morphology_analysis
        for word in morph_an.find_all('word'):
            document.append(m)
        
        xml_out = out_file_name(out_dir_sub, in_file)
        with codecs.open(xml_out, 'wb', encoding='utf-8') as f:
            f.write(document.prettify())