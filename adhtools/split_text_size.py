"""Split a text in separate files of a certain size.
"""

import click
import os


def write_output(result, in_file, out_dir, i):
    doc_name = os.path.splitext(os.path.basename(in_file))[0]
    fname = '{}-{:05}.txt'.format(doc_name, i)
    fname = os.path.join(out_dir, fname)
    with open(fname, 'wb') as fo:
        for part in result:
            fo.write(part)


@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.option('--size', '-s', default=3000)
@click.option('--out_dir', '-o', default=os.getcwd(), type=click.Path())
def split_text(in_file, size, out_dir):
    """Tool that splits a text file into multiple files of a certain size.

    The size is measured in bytes. The text is spilt on the first space after
    the desired file size is reached. So the file size slightly differs between
    files.

    The file is split on a space, so every text contains whole words.
    We chose this way of splitting, because many Arabic texts do not contain
    puntucation.
    """

    result = []
    num = 0

    with open(in_file, "rb") as f:
        bts = f.read(size)
        while bts:
            result.append(bts)

            # find the next whitespace
            byte = f.read(1)
            while byte:
                result.append(byte)
                if byte == b' ' or byte == b'\n':
                    write_output(result, in_file, out_dir, num)

                    result = []
                    num += 1
                    break
                byte = f.read(1)

            bts = f.read(size)
    if result != []:
        write_output(result, in_file, out_dir, num)
        num += 1

    click.echo('The text was split into {} pieces.'.format(num))


if __name__ == '__main__':
    split_text()
