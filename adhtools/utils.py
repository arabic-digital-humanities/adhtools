import pandas as pd
from lxml import etree
from tqdm import tqdm
import re

def stemmer_xml2df(fname):
    result = []
    
    # Extract the words
    context = etree.iterparse(fname, events=('end', ), tag=('word'))
    for event, elem in context:
        stem = None
        for a in elem.getchildren():
            if a.tag == 'analysis':
                stem = a.attrib['stem']
        result.append({'word': elem.attrib['value'], 'proposed_root': stem})
        
        # make iteration over context fast and consume less memory
        #https://www.ibm.com/developerworks/xml/library/x-hiperfparse
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    
    return pd.DataFrame(result)

def analyzer_xml2df(fname):
    result = []
    
    # Extract the words
    context = etree.iterparse(fname, events=('end', ), tag=('word'))
    for event, elem in context:
        word = elem.attrib['value']
        #print(repr(word))
        if word != '':
            roots = []
            for a in elem.getchildren():
                if a.tag == 'analysis':
                    try:
                        roots.append(a.attrib['root'])
                    except:
                        pass
            roots = list(set(roots))
            if len(roots) == 0:
                roots.append('NOANALYSIS')
            result.append({'word': elem.attrib['value'], 'proposed_root': '\\'.join(roots)})
        
        # make iteration over context fast and consume less memory
        #https://www.ibm.com/developerworks/xml/library/x-hiperfparse
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    
    return pd.DataFrame(result)


def read_file_analyzer(in_file, field='proposed_root'):
    data = analyzer_xml2df(in_file)
    return(list(data[field]))


def read_file_stemmer(in_file, field='proposed_root'):
    data = stemmer_xml2df(in_file)
    return(list(data[field]))


def corpus_wordlist(in_files, analyzer=True, field='proposed_root'):
    for in_file in in_files:
        if analyzer:
            ws = read_file_analyzer(in_file, field=field)
        else:
            ws = read_file_stemmer(in_file, field=field)
        
        yield(ws)
        
def corpus_str(in_files, analyzer=True, field='proposed_root'):
    for ws in corpus_wordlist(in_files, analyzer=analyzer, field=field):
        yield ' '.join(list(ws))
        
        
def normalize_arabic(text):
    # Remove non-arabic characters
    nonarab_chars = '[^\u0621-\u064A ]'
    text = re.sub(nonarab_chars, '', text)
    text = text.strip()
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    return text