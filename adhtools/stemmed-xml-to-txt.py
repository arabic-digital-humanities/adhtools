import click
import codecs
import os
import re
from lxml import etree

@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--nr_tokens', '-n', default=300, type=click.INT)
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def stemmed_xml_to_txt(in_file, out_dir, nr_tokens):

    context = etree.iterparse(in_file.name, events=('end', ),
                                  tag=('analysis'))
    
    fn_out = os.path.basename(in_file.name).replace('xml', 'txt')
    with open(os.path.join(out_dir, fn_out), 'w') as f_out:
        i = 1
        sentence = []
        for event, elem in context:
            sentence.append(elem.attrib['stem'] )
            if i%nr_tokens==0:
                f_out.write(' '.join(sentence)+'\n')
                sentence = []
            i += 1
           
        if len(sentence)>0:
            f_out.write(' '.join(sentence)+'\n')
            
if __name__ == '__main__':
    stemmed_xml_to_txt()
