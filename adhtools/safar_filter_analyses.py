#!/usr/bin/env python
import click
import os
import codecs

from lxml import etree
from tqdm import tqdm

from nlppln.utils import out_file_name


@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def safar_filter_analyses(in_file, out_dir):
    analyses = []

    xml_out = out_file_name(out_dir, in_file)
    click.echo(xml_out)
    with codecs.open(xml_out, 'wb') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n'.encode('utf-8'))
        f.write('<document>\n'.encode('utf-8'))
        context = etree.iterparse(in_file, events=('start', ),
                                  tag=('morphology_analysis'))
        for event, elem in context:
            num_words = elem.attrib['total_words']
            break
        del context

        first_word = True
        context = etree.iterparse(in_file, events=('end', ),
                                  tag=('word', 'analysis', 'metadata',
                                       'markers'))
        for event, elem in tqdm(context):
            if elem.tag == 'word':
                if first_word:
                    tag = '<morphology_analysis total_words="{}">\n'. \
                          format(num_words)
                    f.write(tag.encode('utf-8'))
                    first_word = False
                analyses = list(set(analyses))
                tag = '<word total_analysis="{}" value="{}" w_id="{}">\n'
                tag = tag.format(len(analyses), elem.attrib['value'],
                                 elem.attrib['w_id'])
                f.write(tag.encode('utf-8'))
                f.write(b''.join(analyses))
                f.write('</word>\n'.encode('utf-8'))

                analyses = []
            elif elem.tag == 'analysis':
                for attribute in ('a_id', 'vowled', 'pattern', 'prefix',
                                  'suffix', 'additional_info', 'caze',
                                  'gender', 'mood', 'pos', 'type', 'impartial',
                                  'transitive', 'number'):
                    try:
                        del elem.attrib[attribute]
                    except KeyError:
                        pass
                # Setting method to html (instead of xml) fixes problems
                # with writing Arabic characters in the value attribute of
                # the word element.
                analyses.append(etree.tostring(elem, encoding='utf-8',
                                               method='html'))
            elif elem.tag == 'metadata':
                f.write(etree.tostring(elem, encoding='utf-8'))

            elif elem.tag == 'markers':
                f.write(etree.tostring(elem, encoding='utf-8'))

            # make iteration over context fast and consume less memory
            # https://www.ibm.com/developerworks/xml/library/x-hiperfparse
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context

        f.write('</morphology_analysis>\n'.encode('utf-8'))
        f.write('</document>\n'.encode('utf-8'))


if __name__ == '__main__':
    safar_filter_analyses()
