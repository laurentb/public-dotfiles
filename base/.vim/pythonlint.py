#!/usr/bin/env python
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from pyflakes.scripts.pyflakes import main
try:
    main()
except SystemExit, e:
    pass

import pep8
pep8.MAX_LINE_LENGTH = 120
from sys import argv
argv.insert(1, '--repeat')
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=ImportWarning)
    from pkg_resources import load_entry_point
load_entry_point('pep8', 'console_scripts', 'pep8')()

raise e
