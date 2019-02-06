#!/usr/bin/env python
"""Merge separate SAFAR output files into a single output file.

Before stemming or analyzing, the text files are split into multiple small
files. This is done to prevent SAFAR from running out of memory when it has
to write a very large XML file to disk. After stemming or analyzing, the
xml output files for the split text have to be combined into a single output
xml file. This file contains the command line tool to do this.
"""
import click
import os
import codecs
import tqdm
import tempfile

from lxml import etree

from nlppln.utils import create_dirs, get_files, out_file_name


def is_marked(name):
    """Returns True if the input file contains either a header or a Quran quote

    The file name is used to determine whether the file contains a header or a
    Quran quote.
    """
    if 'header' in name:
        return True
    if 'QQuote' in name or 'HQuote' in name:
        return True
    return False


def marker_xml(marker, marker_words, w_ids, attrib, value):
    """Returns marker xml given words and word ids.

    For headers, this function returns a byte string like:
    <header level="1" text="Some Arabic text">
      <ref id="145795"/>
      <ref id="145796"/>
      <ref id="145797"/>
      <ref id="145798"/>
      <ref id="145799"/>
    </header>

   And for Quran/Hadith quotes:
   <quote type="quran|hadith" text="Some Arabic text">
     <ref id="3824"/>
     <ref id="3825"/>
     <ref id="3826"/>
     <ref id="3827"/>
     <ref id="3828"/>
    </quote>
    """
    xml = []
    xml.append('<{} {}="{}" text="{}">\n'.format(marker, attrib, value,
               ' '.join(marker_words)).encode('utf-8'))
    for w_id in w_ids:
        xml.append('  <ref id="{}"/>\n'.format(w_id).encode('utf-8'))
    xml.append('</{}>\n'.format(marker).encode('utf-8'))

    return b''.join(xml)


@click.command()
@click.argument('in_dir', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def merge_safar_xml(in_dir, out_dir):
    """Command line tool that merges SAFAR xml files into a single file.
    """
    create_dirs(out_dir)

    in_files = get_files(in_dir)

    analysis_tag = 'morphology_analysis'

    words = []
    metadata = b'<metadata></metadata>'
    markers = {}
    marker_words = {}

    if len(in_files) == 0:
        msg = 'Unable to merge xml files, because the input directory is ' \
              'empty.'
        raise(ValueError(msg))
    else:
        num_words = 0

        fname = os.path.basename(in_files[0]).split('-')[0]
        xml_out = out_file_name(out_dir, u'{}.xml'.format(fname))

        click.echo('Reading xml files')
        (fd, tmpfile) = tempfile.mkstemp()
        with codecs.open(tmpfile, 'wb') as words:
            for i, fi in tqdm.tqdm(enumerate(in_files)):
                # Check whether we are dealing with a marker
                m = is_marked(os.path.basename(fi))
                if m:
                    mname = os.path.basename(fi).rsplit('-', 1)[0]

                if i == 0:
                    # check whether the analysis_tag should be stemmer_analysis
                    # and extract the metadata
                    context = etree.iterparse(fi, events=('end', ),
                                              tag=('stemmer_analysis',
                                                   'metadata'))
                    for event, elem in context:
                        if elem.tag == 'stemmer_analysis':
                            analysis_tag = elem.tag
                        elif elem.tag == 'metadata':
                            metadata = etree.tostring(elem, encoding='utf-8')

                # Check whether we are dealing with a marker
                if m:
                    if fname not in markers.keys():
                        markers[mname] = []
                        marker_words[mname] = []
                # Extract the words
                context = etree.iterparse(fi, events=('end', ), tag=('word'))
                for event, elem in context:
                    num_words += 1
                    elem.attrib['w_id'] = str(num_words)

                    if m:
                        markers[mname].append(str(num_words))
                        marker_words[mname].append(elem.attrib['value'])

                    # Setting method to html (instead of xml) fixes problems
                    # with writing Arabic characters in the value attribute of
                    # the word element.
                    words.write(etree.tostring(elem, encoding='utf-8',
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

            with codecs.open(tmpfile, 'rb') as words_file:
                for line in tqdm.tqdm(words_file):
                    f.write(line)

            f.write('  </{}>\n'.format(analysis_tag).encode('utf-8'))

            f.write(b'<markers>\n')

            for fname, w_ids in markers.items():
                if 'header' in fname:
                    level = fname.rsplit('-', 1)[1]
                    f.write(marker_xml('header', marker_words[fname], w_ids,
                                       'level', level))
                else:
                    if 'QQuote' in fname:
                        typ = 'quran'
                    else:
                        typ = 'hadith'
                    f.write(marker_xml('quote', marker_words[fname], w_ids,
                                       'type', typ))

            f.write(b'</markers>\n')

            f.write(b'</document>\n')
        os.remove(tmpfile)


if __name__ == '__main__':
    merge_safar_xml()
