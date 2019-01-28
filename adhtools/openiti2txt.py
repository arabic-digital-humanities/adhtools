"""Remove metadata from a text in OpenITI format.

Do we use this command?
"""
#!/usr/bin/env python
import click
import codecs
import os

from nlppln.utils import create_dirs, out_file_name


@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def openiti2txt(in_file, out_dir):
    """Remove metadata from a text in OpenITI format.
    """
    create_dirs(out_dir)

    text = []
    for line in in_file:
        # Ignore metadata in the file and openITI header
        if not line.startswith('#META#') and line != '######OpenITI#\n':
            text.append(line)

    # TODO: optionally remove other openITI tags

    text = u''.join(text)
    fname = out_file_name(out_dir, in_file.name, ext='txt')
    with codecs.open(fname, 'wb', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    openiti2txt()
