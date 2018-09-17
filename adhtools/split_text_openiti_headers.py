import click
import codecs
import os
import re


def smart_strip(text, to_remove=('\u200f')):
    text = ''.join(list(filter(lambda char: char not in to_remove, text)))
    return text.strip()


@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def split_text(in_file, out_dir):
    text = in_file.read()

    regex = r'\#\#\# (\|+) (.+?)\n'

    start = 0
    i = 0

    doc_name = os.path.splitext(os.path.basename(in_file.name))[0]

    for m in re.finditer(regex, text):
        prev_text = text[start:m.start()]
        prev_text = smart_strip(prev_text)

        if len(prev_text) > 0:
            fname = '{}-{:05}.txt'.format(doc_name, i)
            fname = os.path.join(out_dir, fname)
            with codecs.open(fname, 'w', encoding='utf-8') as f:
                f.write(prev_text)
                f.write('\n')
            i += 1

        level = len(m.group(1))
        header = smart_strip(m.group(2))
        if len(header) > 0:
            fname = '{}-{:05}-header-{}.txt'.format(doc_name, i, level)
            fname = os.path.join(out_dir, fname)
            with codecs.open(fname, 'w', encoding='utf-8') as f:
                f.write(header)
                f.write('\n')
            i += 1

        start = m.end()

    # write final piecs of text
    prev_text = text[start:]
    prev_text = smart_strip(prev_text)

    if len(prev_text) > 0:
        fname = '{}-{:05}.txt'.format(doc_name, i)
        fname = os.path.join(out_dir, fname)
        with codecs.open(fname, 'w', encoding='utf-8') as f:
            f.write(prev_text)
            f.write('\n')
        i += 1

    click.echo('The text was split into {} pieces.'.format(i))

if __name__ == '__main__':
    split_text()
