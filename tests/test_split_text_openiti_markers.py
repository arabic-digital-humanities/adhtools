# -*- coding: utf-8 -*-
import os
import glob

from click.testing import CliRunner

from adhtools.split_text_openiti_headers import split_text, smart_strip


# Documentation about testing click commands: http://click.pocoo.org/5/testing/
def test_split_text_openiti_headers():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs('in')
        os.makedirs('out')

        with open('in/test.txt', 'w') as f:
            content = '### | This is a header\n\nThis is the text.\n\n' \
                      '### || Another header\n\nMore text.\n' \
                      '@QB@This is a quran quote@QE@\n' \
                      'Some in between text.\n' \
                      '@HB@This is an hadith quote@HE@\n' \
                      'The final piece of text'
            f.write(content)

        result = runner.invoke(split_text, ['in/test.txt', '--out_dir', 'out'])

        assert result.exit_code == 0
        assert result.output == 'The text was split into 8 pieces.\n'

        file_contents = ['This is a header\n', 'This is the text.\n',
                         'Another header\n', 'More text.\n',
                         'This is a quran quote\n', 'Some in between text.\n',
                         'This is an hadith quote\n',
                         'The final piece of text\n']
        out_files = glob.glob('out/test-0000*.txt')
        out_files.sort()
        for i, fn in enumerate(out_files):
            assert os.path.exists(fn), 'File {} does not exist'.format(fn)
            with open(fn) as f:
                out = f.read()
            assert file_contents[i] == out, 'Mistake in file {}'.format(fn)


def test_smart_strip():
    assert smart_strip('\n\n\n\n\n\n\n\u200f') == ''
    assert smart_strip('quran') == 'quran'
