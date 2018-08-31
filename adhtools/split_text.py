import click
import codecs
import os
import re


@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--regex', multiple=True)
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def split_text(in_file, out_dir, regex):
    text = in_file.read()
    # split based on the regex
    regex = [re.escape(r) for r in regex]
    regex = '|'.join(regex)
    groups = re.split(regex, text)

    # Write out the textfiles
    doc_name = os.path.splitext(os.path.basename(in_file.name))[0]
    for i, subtext in enumerate(groups):
        subtext = subtext.strip()
        if len(subtext) > 0:
            fname = '{}-{:05}.txt'.format(doc_name, i)
            fname = os.path.join(out_dir, fname)

            with codecs.open(fname, 'wb', encoding='utf-8') as f:
                f.write(subtext)
    click.echo('The text was split into {} pieces.'.format(i))

if __name__ == '__main__':
    split_text()
