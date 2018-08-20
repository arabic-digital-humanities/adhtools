#!/usr/bin/env python
import click
import codecs
import os

from lxml import etree

from nlppln.utils import out_file_name, create_dirs


@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.argument('in_file_meta', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def safar_add_metadata(in_file, in_file_meta, out_dir):
    create_dirs(out_dir)

    analysis_tag = 'morphology_analysis'
    total_words = '0'

    words = []
    metadata = '<metadata></metadata>'

    # check whether the analysis_tag should be stemmer_analysis
    context = etree.iterparse(in_file, events=('end', ),
                              tag=('stemmer_analysis', 'morphology_analysis'))
    for event, elem in context:
        if elem.tag == 'stemmer_analysis':
            analysis_tag = elem.tag
        total_words = elem.attrib['total_words']

    # Extract the words
    context = etree.iterparse(in_file, events=('end', ), tag=('word'))
    for event, elem in context:
        # Setting method to html (instead of xml) fixes problems
        # with writing Arabic characters in the value attribute of
        # the word element.
        words.append(etree.tostring(elem, encoding='utf-8', method='html'))

        # make iteration over context fast and consume less memory
        # https://www.ibm.com/developerworks/xml/library/x-hiperfparse
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    # Extract the metadata
    with codecs.open(in_file_meta, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if lines[0].startswith('<?'):
        lines = lines[1:]
    metadata = ''.join(lines)

    # Write output
    xml_out = out_file_name(out_dir, in_file)
    with codecs.open(xml_out, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(b'<document>\n')

        f.write(metadata.encode('utf-8'))

        tag = '  <{} total_words="{}">\n'.format(analysis_tag, total_words)
        f.write(tag.encode('utf-8'))

        for w in words:
            f.write(w)

        f.write('  </{}>\n'.format(analysis_tag).encode('utf-8'))
        f.write(b'</document>\n')


if __name__ == '__main__':
    safar_add_metadata()
