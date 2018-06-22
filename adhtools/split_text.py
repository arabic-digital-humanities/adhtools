import click
import codecs
import os
import re

@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
@click.option('--regex', '-r', default='@K@')
def split_text(in_file, out_dir, regex):
    all_text = in_file.read()
    
    metadata_delimiter = "#META#Header#End#\n"
    split_metadata = re.split(metadata_delimiter, all_text)
    
    if len(split_metadata)==2:
        metadata = split_metadata[0]
        text = split_metadata[1]

        # split based on the regex
        groups = re.split(regex, text)

        # Write out the textfiles
        doc_name = os.path.splitext(os.path.basename(in_file.name))[0]
        for i, subtext in enumerate(groups):
            subtext = subtext.strip()
            if len(subtext) > 0:
                fname = '{}.{:05}.txt'.format(doc_name, i)

                with codecs.open(os.path.join(out_dir, fname), 'wb', encoding='utf-8') as f:
                    f.write(metadata)
                    f.write(metadata_delimiter)
                    f.write(subtext)
    else:
        print("No valid OpenITI")
            
if __name__ == '__main__':
    split_text()
