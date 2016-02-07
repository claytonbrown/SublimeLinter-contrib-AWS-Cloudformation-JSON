#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Clayton Brown
# Copyright (c) 2016 Clayton Brown
#
# License: MIT
#

"""This module exports the AWSCloudformationJSON plugin class."""

import json
import sys
import os.path
import re
import sublime
from SublimeLinter.lint import PythonLinter
# save and reference preferenses etc
from SublimeLinter.lint import persist
# If the linter outputs errors only on stderr or stdout, set error_stream to util.STREAM_STDERR or util.STREAM_STDOUT
from SublimeLinter.lint import util


# packaged dependencies is the folder in our plugin
sys.path.append(os.path.join(os.path.dirname(__file__), "./dist/"))
import boto3

if persist.settings.get('debug'):
    persist.printf('{} dependencies: {}'.format(__name__, boto3))
    persist.printf('{} dependencies: {}'.format(__name__, persist))
    persist.printf('{} dependencies: {}'.format(__name__, util))


"""
awscli
boto
botocore
colorama
concurrent
dateutil
docutils
jmespath
pyasn1
rsa
six.py
"""

# http://www.sublimelinter.com/en/latest/linter_settings.html


class AWSCloudformationJSON(PythonLinter):

    """Provides an interface to json.loads()."""

    syntax = 'cloudformation'
    cmd = None
    loose_regex = re.compile(r'^.+: (?P<message>.+) in \(data\):(?P<line>\d+):(?P<col>\d+)')
    strict_regex = re.compile(r'^(?P<message>.+):\s*line (?P<line>\d+) column (?P<col>\d+)')
    regex = loose_regex
    defaults = {
        'strict': True
    }
    extensions = [
        '.template',
        '.cf.json',
        '.cf',
    ]

    aws_cloudformation_api = None

    @classmethod
    def initialize(self):
        """Initialize the class after plugin load."""

        if self.module is None:
            print("error no class module")
            return

        try:
            print(boto3)
            print("Initialised class module: %s" % (self.module))
        except Exception as e:
            print(e)

    def run(self, cmd, code):
        """Attempt to parse code as JSON, return '' if it succeeds, the error message if it fails."""

        # Use ST's loose parser for its setting files.
        strict = os.path.splitext(self.filename)[1] not in self.extensions

        try:
            if strict:
                self.__class__.regex = self.strict_regex

                # establish basic JSON compliance with in built python JSON library
                template = json.loads(code)

                # now validate against the AWS api
                cfn = boto3.client('cloudformation')
                template = cfn.validate_template(TemplateBody=code)
                print(template)
            else:
                self.__class__.regex = self.loose_regex
                sublime.decode_value(code)

            return ''

        except ValueError as err:
            return str(err)

    def get_report(self):
        """Return the Report class for use by flake8."""
        """
        if self.report is None:
            from pep8 import StandardReport

            class Report(StandardReport):

                ""Provides a report in the form of a single multiline string, without printing.""

                def get_file_results(self):
                    ""Collect and return the results for this file.""
                    self._deferred_print.sort()
                    results = ''

                    for line_number, offset, code, text, doc in self._deferred_print:
                        results += '{path}:{row}:{col}: {code} {text}\n'.format_map({
                            'path': self.filename,
                            'row': self.line_offset + line_number,
                            'col': offset + 1,
                            'code': code,
                            'text': text
                        })

                    return results

            self.__class__.report = Report
        """
        return self.report
