#!/usr/bin/env python
import click
import os
import codecs
import tqdm

from lxml import etree

from nlppln.utils import create_dirs, get_files, out_file_name


@click.command()
@click.argument('in_dir', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def merge_safar_xml(in_dir, out_dir):
    create_dirs(out_dir)

    in_files = get_files(in_dir)

    analysis_tag = 'morphology_analysis'

    words = []
    metadata = b'<metadata></metadata>'

    if len(in_files) == 0:
        msg = 'Unable to merge xml files, because the input directory is ' \
              'empty.'
        raise(ValueError(msg))
    else:
        num_words = 0

        fname = os.path.basename(in_files[0]).rsplit('-', 1)[0]
        xml_out = out_file_name(out_dir, u'{}.xml'.format(fname))

        click.echo('Reading xml files')
        for i, fi in tqdm.tqdm(enumerate(in_files)):
            if i == 0:
                # check whether the analysis_tag should be stemmer_analysis
                # and extract the metadata
                context = etree.iterparse(fi, events=('end', ),
                                          tag=('stemmer_analysis', 'metadata'))
                for event, elem in context:
                    if elem.tag == 'stemmer_analysis':
                        analysis_tag = elem.tag
                    elif elem.tag == 'metadata':
                        metadata = etree.tostring(elem, encoding='utf-8')

            # Extract the words
            context = etree.iterparse(fi, events=('end', ), tag=('word'))
            for event, elem in context:
                num_words += 1
                elem.attrib['w_id'] = str(num_words)

                # Setting method to html (instead of xml) fixes problems
                # with writing Arabic characters in the value attribute of
                # the word element.
                words.append(etree.tostring(elem, encoding='utf-8',
                                            method='html'))

                # make iteration over context fast and consume less memory
                # https://www.ibm.com/developerworks/xml/library/x-hiperfparse
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
            del context

        # write the output
        click.echo('Writing output')
        with codecs.open(xml_out, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(b'<document>\n')

            f.write(metadata)

            tag = '  <{} total_words="{}">\n'.format(analysis_tag, num_words)
            f.write(tag.encode('utf-8'))

            for w in words:
                f.write(w)

            f.write('  </{}>\n'.format(analysis_tag).encode('utf-8'))
            f.write(b'</document>\n')


if __name__ == '__main__':
    merge_safar_xml()
