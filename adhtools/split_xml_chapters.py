"""Tool for splitting SAFAR analyzer XML with header information into chapters.

The result is a SAFAR XML file for each chapter. If the input XML file does not
contain header information, the input file is copied.
"""
import click
import codecs
import os
from lxml import etree
import codecs
import shutil
import copy
from tqdm import tqdm

from nlppln.utils import out_file_name

def write_xml(xml_out, metadata, words, header_titles, analysis_tag = 'morphology_analysis'):
    """Write an XML file for a chapter.
    """
    total_words = len(words)
    with codecs.open(xml_out, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(b'<document>\n')

        ## Add metadata
        metadata_elem = copy.copy(metadata)
        for l, title in enumerate(header_titles):
            if title == '':
                title = '-'
            metadata_elem.append(etree.fromstring('<meta name="Level{}Title">{}</meta>'.format(l+1, title)))
        #metadata_elem.append(etree.fromstring('<meta name="VolumeTitle">{}</meta>'.format(lev1_title)))
        #metadata_elem.append(etree.fromstring('<meta name="ChapterTitle">{}</meta>'.format(lev2_title)))

        metadata_elem.append(etree.fromstring('<meta name="ChapterLength">{}</meta>'.format(len(words))))

        f.write(etree.tostring(metadata_elem, encoding='utf-8', pretty_print=True))
        f.write(b'\n')

        tag = '<{} total_words="{}">\n'.format(analysis_tag, total_words)
        f.write(tag.encode('utf-8'))

        for w in words:
            f.write(w)

        f.write('</{}>\n'.format(analysis_tag).encode('utf-8'))

        #f.write(markers)

        f.write(b'</document>\n')


def analyzer_xml2words_and_headers(fname):
    """Split SAFAR analyzer XML into words, headers and metadata.
    """
    words = {}
    headers = {}
    metadata = etree.fromstring('<metadata></metadata>')

    # Extract the words
    context = etree.iterparse(fname, events=('end', ),
                              tag=('word', 'header', 'metadata'))
    for event, elem in tqdm(context, desc='Extracting data'):
        if elem.tag == 'word':
            w_id = elem.attrib['w_id']
            # Setting method to html (instead of xml) fixes problems
            # with writing Arabic characters in the value attribute of
            # the word element.
            words[int(w_id)] = etree.tostring(elem, encoding='utf-8', method='html')
        if elem.tag == 'header':
            level = int(elem.attrib['level'])
            if level not in headers:
                headers[level] = {}

            header_title = elem.attrib['text']
            for ref in elem.getchildren():
                if ref.tag == 'ref':
                    headers[level][int(ref.attrib['id'])] = header_title
        if elem.tag == 'metadata':
            metadata = copy.copy(elem)
        # make iteration over context fast and consume less memory
        # https://www.ibm.com/developerworks/xml/library/x-hiperfparse
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    del context

    return words, headers, metadata


def get_out_file_name(doc_name, out_dir, i):
    """Generate name for the output file that contains a chapter.

    The output name is based on the name of the input file and an index.
    """
    fname = '{}-{:05}.xml'.format(doc_name, i)
    fname = out_file_name(out_dir, fname)
    return fname

def write_chapters(words, headers, metadata, xml_file, out_dir, levels):
    """Write a file for the specified levels.

    This function divides the words into chapters (based on the level/header
    information) and writes a file for each specified level.

    By default, the text is split on all headers headers that are available in
    the input XML file.
    """
    doc_name = os.path.splitext(os.path.basename(xml_file))[0]
    if levels is None:
        levels = len(headers.keys())
    header_ids = [headers.get(i, {}).keys() for i in range(1, levels+1)]
    if(len(header_ids)>0):
        # do the stuff
        print('Available headers: {}'.format(list(headers.keys())))
        text = []
        is_header = [False]*levels
        i = 0
        header_titles = ['']*levels
        for wid, word in words.items():
            for l in range(1, levels+1):
                if wid in headers.get(l,{}):
                    if not is_header[l-1]:
                        if len(text) > 0:
                            # start of new header
                            # write text to file
                            fname = get_out_file_name(doc_name, out_dir, i)
                            write_xml(fname, metadata, text, header_titles=header_titles)
                            i += 1

                        #reset - also when text is zero
                        text = []
                        header_titles[l-1] = headers[l][wid]
                        is_header[l-1] = True
                else:
                    is_header[l-1] = False
            text.append(word)

        # Also write away the last chapter
        if len(text) > 0:
            # write text to file
            fname = get_out_file_name(doc_name, out_dir, i)
            write_xml(fname, metadata, text, header_titles=header_titles)
    else:
        # no header information, just copy the input file
        print('No headers in', doc_name)
        fo = out_file_name(out_dir, xml_file)
        if os.path.abspath(xml_file) != fo:
            shutil.copy2(xml_file, fo)

@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.option('--levels', '-l', default=None, type=int)
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def split_xml_chapters(in_file, levels, out_dir):
    """Split SAFAR analyzer XML with header information into chapters.
    """
    words, headers, metadata = analyzer_xml2words_and_headers(in_file)

    write_chapters(words, headers, metadata, in_file, out_dir, levels)

if __name__ == '__main__':
    split_xml_chapters()
