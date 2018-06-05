import click
import codecs
import os
import re

@click.command()
@click.argument('in_file', type=click.File(encoding='utf-8'))
@click.option('--verbose', '-v', default=False, is_flag=True)
def validate(in_file, verbose):
    content = in_file.read()
    
    # Check that the file starts with the OpenITI identifier
    assert content.startswith('######OpenITI#'), 'File does not start with OpenITI identifier'
    
    # Check that there is a metadata section
    metadata_delimiter = '#META#Header#End#\n'
    split_metadata = re.split(metadata_delimiter, content)
    assert len(split_metadata) != 1, 'There is no metadata end delimiter'
    assert len(split_metadata) == 2, 'There are multiple metadata end delimiters'
    
    # Check format of meta data 
    metadata = split_metadata[0]
    for i, line in enumerate(metadata.split('\n')[1:]):
        if line != '':
            match = re.match('#META#\s\d{3}\.\w*\s::\s.*', line)
            assert match is not None, 'Metadata line {} does not comply with format'.format(i+1)
    
    text = split_metadata[1]
    
    #Verbose: print statistics
    if verbose:
        pages = re.findall('PageV(\d{2})P(\d{3})', text)
        print('Number of pages: {}, number of unique pages: {}'.format(len(pages), len(set(pages))))
        
        chapters = re.findall('^### \|\s', content, re.MULTILINE)
        print('Number of chapters: {}'.format(len(chapters)))
        
        sections = re.findall('^### \|\|\s', content, re.MULTILINE)
        print('Number of sections: {}'.format(len(sections)))
        
        subsections = re.findall('^### \|\|\|\s', content, re.MULTILINE)
        print('Number of subsections: {}'.format(len(subsections)))
        

if __name__ == '__main__':
    validate()