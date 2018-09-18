# -*- coding: utf-8 -*-
import os

from click.testing import CliRunner

from adhtools.split_text_size import split_text


# Documentation about testing click commands: http://click.pocoo.org/5/testing/
def test_split_text_size():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs('in')
        os.makedirs('out')

        with open('in/test.txt', 'w') as f:
            content = '12345 123456 12345 12345678 1234567\n' \
                      '1234 12345 123456 12345 12345-'
            f.write(content)

        result = runner.invoke(split_text, ['in/test.txt', '--size', '5',
                                            '--out_dir', 'out'])

        assert result.exit_code == 0
        assert result.output == 'The text was split into 9 pieces.\n'

        file_contents = ['12345 ', '123456 ', '12345 ', '12345678 ',
                         '1234567\n', '1234 12345 ', '123456 ', '12345 ',
                         '12345-']
        for i in range(9):
            fname = 'out/test-0000{}.txt'.format(i)
            assert os.path.exists(fname), 'File {} does not exist'.format(i)
            with open(fname) as f:
                out = f.read()
            assert file_contents[i] == out, 'Mistake in file {}'.format(i)
