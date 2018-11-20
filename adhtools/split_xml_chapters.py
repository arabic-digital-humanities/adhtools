import click
import codecs
import os
from lxml import etree
import codecs
import shutil
import copy
from tqdm import tqdm

from nlppln.utils import out_file_name

def write_xml(xml_out, metadata, words, analysis_tag = 'morphology_analysis', lev1_title='', lev2_title=''):
    total_words = len(words)
    with codecs.open(xml_out, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(b'<document>\n')

        ## Add metadata
        if lev1_title=='':
            lev1_title = '-'
        if lev2_title=='':
            lev2_title = '-'
        metadata_elem = copy.copy(metadata)
        metadata_elem.append(etree.fromstring('<meta name="VolumeTitle">{}</meta>'.format(lev1_title)))
        metadata_elem.append(etree.fromstring('<meta name="ChapterTitle">{}</meta>'.format(lev2_title)))
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
    fname = '{}-{:05}.xml'.format(doc_name, i)
    fname = out_file_name(out_dir, fname)
    return fname

def write_chapters(words, headers, metadata, xml_file, out_dir):
    doc_name = os.path.splitext(os.path.basename(xml_file))[0]
    header_ids = list(headers.get(1, {}).keys()) + list(headers.get(2, {}).keys() )
    if(len(header_ids)>0):
        # do the stuff
        print('Available headers: {}'.format(list(headers.keys())))
        text = []
        header1 = False
        header2 = False
        i = 0
        header1_name = ''
        header2_name = ''
        for wid, word in words.items():
            # Level 1 header
            if wid in headers.get(1,{}):
                if header1 == False:
                    if len(text) > 0:
                        # start of new header
                        # write text to file
                        fname = get_out_file_name(doc_name, out_dir, i)
                        write_xml(fname, metadata, text, lev1_title=header1_name, lev2_title=header2_name)
                        i += 1

                    #reset - also when text is zero
                    text = []
                    header1_name = headers[1][wid]
                    header1 = True
            else:
                header1 = False

            # Level 2 header
            if wid in headers.get(2,{}):
                if header2 == False:
                    if len(text) > 0:
                        # start of new header
                        # write text to file
                        fname = get_out_file_name(doc_name, out_dir, i)
                        write_xml(fname, metadata, text, lev1_title=header1_name, lev2_title=header2_name)
                        i += 1

                    #reset
                    text = []
                    header2_name = headers[2][wid]
                    header2 = True
            else:
                header2 = False

            if not header1 and not header2:
                text.append(word)

        # Also write away the last chapter
        if len(text) > 0:
            # write text to file
            fname = get_out_file_name(doc_name, out_dir, i)
            write_xml(fname, metadata, text, lev1_title=header1_name, lev2_title=header2_name)
    else:
        # no header information, just copy the input file
        print('No headers in', doc_name)
        fo = out_file_name(out_dir, xml_file)
        if os.path.abspath(xml_file) != fo:
            shutil.copy2(xml_file, fo)

@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def split_xml_chapters(in_file, out_dir):
    words, headers, metadata = analyzer_xml2words_and_headers(in_file)

    write_chapters(words, headers, metadata, in_file, out_dir)

if __name__ == '__main__':
    split_xml_chapters()
