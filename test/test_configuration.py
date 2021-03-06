from __future__ import with_statement
import os.path
import tempfile

from nose.tools import *
from behave import configuration

# one entry of each kind handled
TEST_CONFIG='''[behave]
outfile=/tmp/spam
paths = /absolute/path
        relative/path
tags = @foo,~@bar
       @zap
format=pretty
       tag-counter
stdout_capture=no
bogus=spam
'''

class TestConfiguration(object):

    def test_read_file(self):
        tn = tempfile.mktemp()
        with open(tn, 'w') as f:
            f.write(TEST_CONFIG)
        d = configuration.read_configuration(tn)
        eq_(d['outfile'], '/tmp/spam')
        eq_(d['paths'], [
            '/absolute/path',
            os.path.normpath(os.path.join(os.path.dirname(tn), 'relative/path')),
            ])
        eq_(d['format'], ['pretty', 'tag-counter'])
        eq_(d['tags'], ['@foo,~@bar', '@zap'])
        eq_(d['stdout_capture'], False)
        ok_('bogus' not in d)

