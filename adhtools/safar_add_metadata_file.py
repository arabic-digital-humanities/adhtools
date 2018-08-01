#!/usr/bin/env python
import click
import codecs
import os
import copy
import six
from bs4 import BeautifulSoup
from nlppln.utils import out_file_name, get_files


@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.argument('in_file_meta', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def safar_add_metadata(in_file, in_file_meta, out_dir):
    doc_id = os.path.splitext(os.path.basename(in_file))[0]
    
    with open(in_file_meta) as fn:
        metadata = BeautifulSoup(fn, 'xml')

    with codecs.open(in_file, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')

    # Make document with a single root element
    document = BeautifulSoup('<document></document>', 'xml')
    md = copy.copy(metadata.metadata)
    document.document.append(md)
    try:
        document.document.append(soup.morphology_analysis)
    except:
        document.document.append(soup.stemmer_analysis)
    
    xml_out = out_file_name(out_dir, in_file)
    with codecs.open(xml_out, 'wb', encoding='utf-8') as f:
        if six.PY2:
            # six.u doesn't work in Python 2 with non-ascii text
            # See https://pythonhosted.org/six/#six.u
            f.write(unicode(document))
        else:
            f.write(str(document))


if __name__ == '__main__':
    safar_add_metadata()
