import click
import codecs
import os
import re

@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.argument('regex')
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def split_text(in_file, out_dir, regex):

    metadata = []
    text = []
    for line in in_file.readlines():
        # TODO: metadata is sometimes inconsistent, (missing # before META,
        # and fields not separated by :: but single :)
        if line.startswith('#META#'):
            metadata.append(line)
        else:
            text.append(line)
       
    metadata = u'\n'.join(metadata)
    text = u'\n'.join(text)

    # split based on the regex
    groups = re.split(regex, text)
    
    # Write out the textfiles
    doc_name = os.path.splitext(os.path.basename(in_file.name))[0]
    for i, subtext in enumerate(groups):
        subtext = subtext.strip()
        if len(subtext) > 0:
            fname = '{}-{:05}.txt'.format(doc_name, i)
            
            with codecs.open(os.path.join(out_dir, fname), 'wb', encoding='utf-8') as f:
                f.write(metadata)
                f.write('\n')
                f.write(subtext)
            
if __name__ == '__main__':
    split_text()
