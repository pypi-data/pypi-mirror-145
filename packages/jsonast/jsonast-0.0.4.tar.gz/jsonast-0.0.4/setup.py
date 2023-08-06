# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonast']

package_data = \
{'': ['*']}

install_requires = \
['jsonml>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'jsonast',
    'version': '0.0.4',
    'description': '',
    'long_description': '# json ast\n<!--\n[![Version](https://img.shields.io/pypi/v/asy)](https://pypi.org/project/asy)\n[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n-->\n\n# Requirement\n\n- Python 3.8+\n\n# Feature\n\n- Specializing in dealing with tree structures\n- Fully compatible with json\n- Can be output as xml\n- Can be output as jsonml\n\n# Motivation\n\n- Where are the standard structures for annotated tree structures?\n- `xml` is the most common, but it would be nice to have a `json` compatible and highly readable structure.\n- `jsonml` is hard to see.\n- `jsonlogic` is good for operations, but not good for grammar.\n\n# Contribute\n\n```\npoetry install\npre-commit install\nsource .venv/bin/activate\nmake\n```\n',
    'author': 'sasano8',
    'author_email': 'y-sasahara@ys-method.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sasano8/jsonast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
