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
from SublimeLinter.lint import persist, PythonLinter, util
# from SublimeLinter.lint import PythonLinter, util
# #from SublimeLinter.lint import Linter




class AWSCloudformationJSON(PythonLinter):

    """Provides an interface to json.loads()."""

    syntax = 'json'
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

    def run(self, cmd, code):
        """Attempt to parse code as JSON, return '' if it succeeds, the error message if it fails."""

        # Use ST's loose parser for its setting files.
        strict = os.path.splitext(self.filename)[1] not in self.extensions

        try:
            if strict:
                self.__class__.regex = self.strict_regex
                template = json.loads(code)
                import boto.cloudformation
                print(boto.cloudformation)
                print(template)
            else:
                self.__class__.regex = self.loose_regex
                sublime.decode_value(code)

            return ''

        except ValueError as err:
            return str(err)