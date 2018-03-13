#!/usr/bin/env python
import click
import codecs
import os
import re
from bs4 import BeautifulSoup
from nlppln.utils import out_file_name


@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def txt2safar_input(in_file, out_dir):

    metadata = {}
    text = []
    for line in in_file.readlines():
        # TODO: metadata is sometimes inconsistent, (missing # before META,
        # and fields not separated by :: but single :)
        if line.startswith('#META#'):
            splitted = line.split(u'::')
            if(len(splitted)==2):
                name, value = line.split(u'::')

                value = value.strip()
                name = name.strip()

                # only save metadata that has a value
                if value != 'NODATA':
                    _, name = name.split(u' ', 1)
                    name = name.replace(u' ', u'_')
                    metadata[name] = value
        else:
            text.append(line)

    # XML file with metadata
    soup = BeautifulSoup('<metadata>', 'xml')
    for k, v in metadata.items():
        tag = soup.new_tag('meta')
        tag['name'] = k
        tag.string = v
        soup.metadata.append(tag)

    xml_out = out_file_name(out_dir, in_file.name, ext='xml')
    with codecs.open(xml_out, 'wb', encoding='utf-8') as f:
        f.write(soup.prettify())

    # write text file per page
    text = u''.join(text)

    # regex with groups
    p_numbers = re.findall('PageV(\d{2})P(\d{3})', text)
    p_numbers.append(('dummy', 'dummy'))

    # same regex without groups
    pages = re.split('PageV\d{2}P\d{3}', text)

    doc_id = os.path.splitext(os.path.basename(in_file.name))[0]

    for (v, p), text in zip(p_numbers, pages):
        text = text.strip()
        if len(text) > 0:
            fname = '{}-V{}P{}.txt'.format(doc_id, v, p)
            with codecs.open(os.path.join(out_dir, fname), 'wb', encoding='utf-8') as f:
                f.write(text)

if __name__ == '__main__':
    txt2safar_input()
