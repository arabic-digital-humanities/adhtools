#!/usr/bin/env python
import click
import codecs
import os
import re

from nlppln.utils import create_dirs, out_file_name

open_iti_meta_data_patterns = [r'######OpenITI#\n', r'#META#(.+)\n']

quotes = r'@(.+?)@'
pages = r'PageV(\d{2})P(\d{3,4})'
milestones = r'Milestone\d+'


@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def openiti2txt(in_file, out_dir):
    create_dirs(out_dir)

    text = in_file.read()

    # remove metadata header
    for p in open_iti_meta_data_patterns:
        text = re.sub(p, '', text)

    # remove other tags
    for p in (quotes, pages, milestones):
        text = re.sub(p, '', text)

    # TODO: normalize spaces

    out_file = out_file_name(out_dir, in_file.name)
    print(out_file)
    with codecs.open(out_file, 'wb', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    openiti2txt()
