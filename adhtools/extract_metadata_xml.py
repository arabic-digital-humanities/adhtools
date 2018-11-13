import click
import codecs
import os
import re
from lxml import etree
import pandas as pd
import glob
import nlppln.utils
from tqdm import tqdm

@click.command()
@click.argument('in_dir', type=click.Path())
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def extract_metadata_xml(in_dir, out_dir):

    result = []
    
    in_files = nlppln.utils.get_files(in_dir)
    for fname in tqdm(in_files, total=len(in_files)):
    
        data = {}
        # Extract the words
        context = etree.iterparse(fname, events=('end', ), tag=('meta'))
        for event, elem in context:
            name = elem.attrib['name']
            value = elem.text
        
            data[name] = value
        
            # make iteration over context fast and consume less memory
            #https://www.ibm.com/developerworks/xml/library/x-hiperfparse
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        data['filename'] = os.path.basename(fname)
        result.append(data)
    result = pd.DataFrame(result)
    result.to_csv(os.path.join(out_dir, 'metadata.csv'))
            
if __name__ == '__main__':
    extract_metadata_xml()
