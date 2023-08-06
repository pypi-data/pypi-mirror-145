# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blocklib', 'blocklib.validation']

package_data = \
{'': ['*'], 'blocklib': ['schemas/*']}

install_requires = \
['bitarray>=2.4.0,<3.0.0',
 'jsonschema>=3.1,<5.0',
 'metaphone>=0.6,<0.7',
 'numpy>=1.20.1,<2.0.0',
 'pydantic>=1.8,<2.0',
 'tqdm>=4.36.1,<5.0.0',
 'typing_extensions>=3.7.4,<5.0.0']

extras_require = \
{'docs': ['nbval>=0.9.6,<0.10.0',
          'Sphinx>=4.1.0,<5.0.0',
          'nbsphinx>=0.8.2,<0.9.0',
          'pandas>=1.3.5,<2.0.0',
          'notebook>=6.2.0,<7.0.0']}

setup_kwargs = {
    'name': 'blocklib',
    'version': '0.1.8',
    'description': 'A library for blocking in record linkage',
    'long_description': '\n[![codecov](https://codecov.io/gh/data61/blocklib/branch/master/graph/badge.svg)](https://codecov.io/gh/data61/blocklib)\n[![Documentation Status](https://readthedocs.org/projects/blocklib/badge/?version=latest)](http://blocklib.readthedocs.io/en/latest/?badge=latest)\n[![Typechecking](https://github.com/data61/blocklib/actions/workflows/typechecking.yml/badge.svg)](https://github.com/data61/blocklib/actions/workflows/typechecking.yml)\n[![Testing](https://github.com/data61/blocklib/actions/workflows/python-test.yml/badge.svg)](https://github.com/data61/blocklib/actions/workflows/python-test.yml)\n[![Downloads](https://pepy.tech/badge/blocklib)](https://pepy.tech/project/blocklib)\n\n\n# Blocklib\n\n\nPython implementations of record linkage blocking techniques. Blocking is a technique that makes\nrecord linkage scalable. It is achieved by partitioning datasets into groups, called blocks and only\ncomparing records in corresponding blocks. This can reduce the number of comparisons that need to be\nconducted to find which pairs of records should be linked.\n\n`blocklib` is part of the **Anonlink** project for privacy preserving record linkage.\n\n\n### Installation\n\nInstall with pip:\n\n    pip install blocklib\n\n### Documents\n\nYou can find comprehensive documentation and tutorials in [readthedocs](http://blocklib.readthedocs.io/en/latest)\n\n### Tests\n\nRun unit tests with `pytest`::\n\n    $ pytest\n\n\n### Discussion\n\nIf you run into bugs, you can file them in our [issue tracker](https://github.com/data61/blocklib/issues)\non GitHub.\n\nThere is also an [anonlink mailing list](https://groups.google.com/forum/#!forum/anonlink)\nfor development discussion and release announcements.\n\nWherever we interact, we strive to follow the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/)\n\n\n### License and Copyright\n\n`blocklib` is copyright (c) Commonwealth Scientific and Industrial Research Organisation (CSIRO).\n\nLicensed under the Apache License, Version 2.0 (the "License"). You may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': 'Wilko Henecka',
    'author_email': 'wilkohenecka@gmx.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/data61/blocklib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
