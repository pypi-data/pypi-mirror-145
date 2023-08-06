"""Package meta data."""

import sys


name = 'sttp'
version = '0.0.3'
author = 'Michael Wright'
author_email = 'mjw@methodanalysis.com'
description = 'Strict Text Template Parsing'
url = 'https://github.com/mwri/sttp'

classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

entry_points = {
    'console_scripts': [],
}

python_requires = '>=3.6'
install_requires = [
    'lark==1.1.2',
]

extras_require = {
    'dev': [
        'lark==1.1.2',
        'pytest==7.1.0',
        'pytest-mock==3.7.0',
        'coverage==6.3.2',
        'Sphinx==4.4.0',
        'sphinx-rtd-theme==1.0.0',
        'black==22.1.0',
    ],
}

package_data = {'sttp.subst': ['grammar.txt']}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        attr_names = sys.argv[1:]
        attr_val = getattr(sys.modules[__name__], attr_names.pop(0))

        def display_val(val):
            if type(attr_val) == str:
                print(val)
            elif type(val) == list:
                for sub_val in val:
                    print(sub_val)
            elif type(val) == dict:
                print(repr(val))

        if type(attr_val) in (str, list):
            display_val(attr_val)
        elif type(attr_val) == dict:
            while len(attr_names) > 0 and type(attr_val) == dict:
                attr_val = attr_val[attr_names.pop(0)]
            display_val(attr_val)
