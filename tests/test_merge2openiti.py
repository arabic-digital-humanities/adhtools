# -*- coding: utf-8 -*-
import pytest
import os
import nltk

from click.testing import CliRunner

# FIXME: import correct methods for testing
from adhtools.merge2openiti2 import tokenize, get_spaces_pattern


@pytest.fixture
def tokenizer():
    try:
        res = nltk.data.find('tokenizers/punkt')
    except LookupError:
        res = nltk.download('punkt')

    return res


def test_tokenize(tokenizer):
    if tokenizer:
        s = 'This is a "test" sentence.'
        tokens = tokenize(s)

        # double quotes should still exist
        assert tokens == ['This', 'is', 'a', '"', 'test', '"', 'sentence', '.']


def test_tokenize_no_newline(tokenizer):
    if tokenizer:
        s = 'This is a "test" sentence.\n'
        tokens = tokenize(s)

        assert tokens == ['This', 'is', 'a', '"', 'test', '"', 'sentence', '.']


def test_get_spaces_pattern(tokenizer):
    if tokenizer:
        s = 'This is a "test" sentence.'
        spaces = get_spaces_pattern(s)

        assert spaces == (' ', ' ', ' ', '', '', ' ', '')


def test_get_spaces_pattern_parentheses(tokenizer):
    if tokenizer:
        s = 'This is a (test) sentence.'
        spaces = get_spaces_pattern(s)

        assert spaces == (' ', ' ', ' ', '', '', ' ', '')


# Documentation about testing click commands: http://click.pocoo.org/5/testing/
#def test_openiti2txt():
#    runner = CliRunner()
#    with runner.isolated_filesystem():
#        os.makedirs('in')
#        os.makedirs('out')

#        # FIXME: create example input file(s)
#        with open('in/test.txt', 'w') as f:
#            content = '\n' \
#                      '\n'
#            f.write(content)

#        # FIXME: update command, options and arguments
#        result = runner.invoke(openiti2txt, ['<argument>', '--out_dir', 'out'])

#        assert result.exit_code == 0

#        # FIXME: What files should exist after command execution?
#        #assert os.path.exists('out/test.xml')
