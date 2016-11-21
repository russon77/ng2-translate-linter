#!/usr/bin/env python3

"""
Copyright (c) <2016> Tristan Kernan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import unittest
import json
import glob
import os
import re
import sys

# to override, i.e. to iterate over separate translation dictionaries, please use <argv[1]>
# DICTIONARY_LOCATION = 'smart-response/i18n/en.json'
DICTIONARY_LOCATION = 'SmartWeb/smart-response/i18n/en.json'
# directory to search for .html and .ts files
SOURCE_DIRECTORY = 'SmartWeb/src'


class TranslationDictionaryTests(unittest.TestCase):
    """
    set of basic tests to confirm dictionary exists, is valid JSON, and has max depth of 1
    """
    def setUp(self):
        try:
            self.dictionary_fp = open(DICTIONARY_LOCATION, 'r')
        except FileNotFoundError:
            self.fail('Could not find dictionary file.')

    def tearDown(self):
        self.dictionary_fp.close()

    def test_is_valid_json(self):
        try:
            json.load(self.dictionary_fp)
        except json.JSONDecodeError:
            self.fail('JSON is not valid, file could not be parsed successfully.')

    def test_duplicate_keys(self):
        # thanks to
        # http://stackoverflow.com/questions/14902299/json-loads-allows-duplicate-keys-in-a-dictionary-overwriting-the-first-value

        def dict_raise_on_duplicates(ordered_pairs):
            d = {}
            for k, v in ordered_pairs:
                if k in d:
                    raise ValueError('duplicate key')
                else:
                    d[k] = v
            return d

        try:
            json.load(self.dictionary_fp, object_pairs_hook=dict_raise_on_duplicates)
        except ValueError:
            self.fail('Duplicate keys found.')

    def test_dictionary_depth(self):
        """
        test whether the translation dictionary is only one level deep
        to test this, check whether each value is a string

        todo: update this to allow nested dictionaries
        :return:
        """
        d = json.load(self.dictionary_fp)

        for k in d:
            self.assertTrue(isinstance(d[k], str), 'Dictionary value was not type str.')


class MissingAndExtraKeysTest(unittest.TestCase):
    def setUp(self):
        try:
            with open(DICTIONARY_LOCATION, 'r') as dict_file:
                self.dictionary = json.load(dict_file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.fail('Could not find dictionary file.')

    def tearDown(self):
        pass

    def test_me(self):
        """
        Fail if there are keys *in use* in a .html or .ts file, but are not present in the translation dictionary.

        todo: update to allow nested dictionaries.
        :return:
        """
        keys_in_use = set()

        html_regex = r"\s*['\"][-_\w]+['\"]\s*\|\s*translate\s*"
        html_prog = re.compile(html_regex)

        ts_regex = r"\.instant\(['\"][-_\w]+['\"]"
        ts_prog = re.compile(ts_regex)

        for ts_filename in glob.iglob(os.path.join(SOURCE_DIRECTORY, '**', '*.ts'), recursive=True):
            with open(ts_filename, 'r') as ts_file:
                ts_file_contents = ts_file.read()
                ts_file_contents_no_whitespace = ''.join(ts_file_contents.split())
                for match in ts_prog.finditer(ts_file_contents_no_whitespace):
                    matched_string = ts_file_contents_no_whitespace[match.start():match.end()]

                    split = matched_string.split('(')
                    key = split[1].replace('\'', '').replace('\"', '')

                    keys_in_use.add(key)

        for html_filename in glob.iglob(os.path.join(SOURCE_DIRECTORY, '**', '*.html'), recursive=True):
            with open(html_filename, 'r') as html_file:
                html_file_contents = html_file.read()
                html_file_contents_no_whitespace = ''.join(html_file_contents.split())
                for match in html_prog.finditer(html_file_contents_no_whitespace):
                    matched_string = html_file_contents_no_whitespace[match.start():match.end()]

                    split = matched_string.split('|')
                    key = split[0].replace('\'', '').replace('\"', '')
                    
                    keys_in_use.add(key)

        keys_in_dictionary = set(_ for _ in self.dictionary.keys() if not _.startswith('-'))

        keys_never_used_from_dictionary = keys_in_dictionary.difference(keys_in_use)
        if len(keys_never_used_from_dictionary):
            print('Keys never used from dictionary', keys_never_used_from_dictionary)

        keys_missing_from_dictionary = keys_in_use.difference(keys_in_dictionary)
        if len(keys_missing_from_dictionary):
            print('Keys missing from dictionary', keys_missing_from_dictionary)

        self.assertEqual(len(keys_missing_from_dictionary), 0, 'Discovered keys in use missing from dictionary.')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        DICTIONARY_LOCATION = sys.argv.pop(1)

        if len(sys.argv) > 1:
            SOURCE_DIRECTORY = sys.argv.pop(1)

    unittest.main()
