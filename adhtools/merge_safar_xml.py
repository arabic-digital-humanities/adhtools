#!/usr/bin/env python
import click
import os
import shutil

from nlppln.utils import get_files, out_file_name, read_xml, write_xml


def get_total_words(soup):
    return int(soup.morphology_analysis['total_words'])


@click.command()
@click.argument('in_dir', type=click.Path(exists=True))
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def merge_safar_xml(in_dir, out_dir):

    in_files = get_files(in_dir)

    if len(in_files) == 1:
        fname = os.path.basename(in_files[0]).split('-')[0]
        xml_out = out_file_name(out_dir, u'{}.xml'.format(fname))

        shutil.copy2(in_files[0], xml_out)

    elif len(in_files) > 1:
        fname = os.path.basename(in_files[0]).split('-')[0]
        xml_out = out_file_name(out_dir, u'{}.xml'.format(fname))

        wd = read_xml(in_files[0])

        total_words = get_total_words(wd)

        for fi in in_files[1:]:
            doc = read_xml(fi)
            tw = get_total_words(doc)
            words = doc.find_all('word')

            # sanity check
            assert len(words) == tw

            for w in words:
                w['w_id'] = int(w['w_id']) + total_words
                wd.morphology_analysis.append(w)

            total_words += tw

        wd.morphology_analysis['total_words'] = total_words
        write_xml(wd, xml_out)


if __name__ == '__main__':
    merge_safar_xml()
