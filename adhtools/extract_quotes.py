#!/usr/bin/env python
import click
import os
import re
from nlppln.utils import out_file_name


@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def extract_quotes(in_file, out_dir):    
	
    data = in_file.read()
    
    qurquotes = re.findall(r'@QB@(.*)@QE@', data)

    fn_out = out_file_name(out_dir, 'quotes_'+os.path.basename(in_file.name), ext='txt')
    print(in_file.name, fn_out)
    if os.path.exists(fn_out):
        os.remove(fn_out)
    with open(fn_out, 'w', encoding='utf-8') as f:
        for q in qurquotes:
            q = q.strip()
            if len(q)>0:
                f.write(re.sub('[^\u0621-\u064A ]', '', q)) #Remove annotations
                f.write('\n')
                
if __name__ == '__main__':
    extract_quotes()
