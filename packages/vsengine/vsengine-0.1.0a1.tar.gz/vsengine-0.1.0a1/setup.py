# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vsengine', 'vsengine.adapters']

package_data = \
{'': ['*']}

install_requires = \
['VapourSynth>=57']

extras_require = \
{'trio': ['trio>=0.20.0,<0.21.0']}

setup_kwargs = {
    'name': 'vsengine',
    'version': '0.1.0a1',
    'description': 'An engine for our vapoursynth previewers',
    'long_description': None,
    'author': 'Sarah',
    'author_email': 'cid+git@cid-chan.moe',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
