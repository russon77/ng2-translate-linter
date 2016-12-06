## ng2-translate-linter

### What and Why
Given a large enough translation dictionary and a large enough project, testing for translation correctness (in this
case, testing if every key used in the project is present in the translation dictionary) is difficult if not impossible 
manually. Thus this script was born. The script runs as several Python unittest test cases in order to benefit from 
the reporting and assertions already in place.

### How
Basic tests use Python's `open()` and `json.load()` methods to test if the dictionary exists and is valid JSON.

The key tests work by removing from each `.html` and `.ts` file all spaces and applying a search regex to find key 
usages. The results are combined into a set (for uniqueness) and use set operations (`set.difference(*others)`) 
to find instances where the key is missing.

### Notes
- Test ignores keys in translation dictionary starting with '-' and empty strings.
- Test ignores spaces in keys *in `.html` and `.ts` files*
    - i.e. `{"MY KEY": "MY TRANSLATION"}` and `{{ 'MY KEY' | translate }}` will fail.
- Test does not support finding arbitrary key usage in plain strings in `.ts` files.
    - i.e. `const x = 'MY_KEY'; translate.instant(x);` is *not* supported.
    - **UPDATE 2016-12-06** keys not found in actual usage are checked for mere presence in the source directory. This 
    finds programmatic used keys in addition to keys in comments, etc.
- Does not support dictionaries with nested keys. Specifically tests *against* this.
- Developed against the Angular 2 rc4 version of `ng2-translate` library.
    
### Requirements
- Python >3.5 due to use of `recursive` flag with `iglob()` 
    
### Usage
- `python3 main.py <path/to/dictionary.json> <path/to/source/files/>`
    
### License
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