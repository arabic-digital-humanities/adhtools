#!/usr/bin/env python
import click
import codecs
import os
import tempfile
import re
import pandas as pd
import six

from lxml import etree
from xml.sax.saxutils import escape
from tqdm import tqdm

from nlppln.utils import out_file_name, create_dirs, remove_ext
from .split_text_openiti_headers import smart_strip


@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.argument('in_file_meta', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def safar_add_metadata(in_file, in_file_meta, out_dir):
    create_dirs(out_dir)

    analysis_tag = None
    total_words = None

    # check whether the analysis_tag should be stemmer_analysis
    with codecs.open(in_file, 'r', encoding='utf-8') as xml_file:
        for line in xml_file:
            if re.search('morphology_analysis', line):
                analysis_tag = 'morphology_analysis'
            elif re.search('stemmer_analysis', line):
                analysis_tag = 'stemmer_analysis'

            m = re.search('total_words="(\d+)"', line)
            if m:
                total_words = m.group(1)

            if analysis_tag is not None and total_words is not None:
                break

    # Extract the words
    click.echo('Extracting tokens')
    (fd, tmpfile) = tempfile.mkstemp()
    with codecs.open(tmpfile, 'wb') as words:
        context = etree.iterparse(in_file, events=('end', ), tag=('word'),
                                  huge_tree=True)
        context = tqdm(context, total=int(total_words))
        for event, elem in context:
            # Setting method to html (instead of xml) fixes problems
            # with writing Arabic characters in the value attribute of
            # the word element.
            words.write(etree.tostring(elem, encoding='utf-8', method='html'))

            # make iteration over context fast and consume less memory
            # https://www.ibm.com/developerworks/xml/library/x-hiperfparse
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context

    # Get the metadata
    md = pd.read_csv(in_file_meta, sep=',|;', index_col='BookURI',
                     encoding='utf-8')
    # make sure the index type is string
    if six.PY2:
        md.index = md.index.map(unicode)
    else:
        md.index = md.index.map(str)

    if '-' in os.path.basename(in_file):
        uri = os.path.basename(in_file).split('-', 1)[0]
    else:
        uri = remove_ext(in_file)

    try:
        md = md.loc[uri]
        metadata = [u'<metadata>']
        for key in md.keys()[1:]:  # skip over order (the old index)
            val = md[key]
            if isinstance(val, six.string_types):
                val = smart_strip(val)
                val = escape(val)
            metadata.append(u'<meta name="{}">{}</meta>'.format(key, val))
        metadata.append(u'<meta name="{}">{}</meta>'.format(
                        '000.BookURI', uri))
        metadata.append(u'</metadata>')

        metadata = u'\n'.join(metadata)
    except KeyError:
        metadata = u'<metadata></metadata>'

    # Write output
    click.echo('Writing output')
    xml_out = out_file_name(out_dir, in_file)
    with codecs.open(xml_out, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(b'<document>\n')

        f.write(metadata.encode('utf-8'))

        tag = '  <{} total_words="{}">\n'.format(analysis_tag, total_words)
        f.write(tag.encode('utf-8'))

        with codecs.open(tmpfile, 'rb') as words_file:
            for line in tqdm(words_file):
                f.write(line)

        f.write('  </{}>\n'.format(analysis_tag).encode('utf-8'))
        f.write(b'</document>\n')

    os.remove(tmpfile)


if __name__ == '__main__':
    safar_add_metadata()
