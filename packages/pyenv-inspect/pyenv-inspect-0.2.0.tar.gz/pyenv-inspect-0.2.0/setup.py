# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyenv_inspect']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyenv-inspect',
    'version': '0.2.0',
    'description': 'An auxiliary library for the virtualenv-pyenv and tox-pyenv-redux plugins',
    'long_description': '# pyenv-inspect\n\nAn auxiliary library for the [virtualenv-pyenv][virtualenv-pyenv] and [tox-pyenv-redux][tox-pyenv-redux] plugins\n\n## Limitations\n\nOnly CPython is supported at the moment.\n\n\n[virtualenv-pyenv]: https://github.com/un-def/virtualenv-pyenv\n[tox-pyenv-redux]: https://github.com/un-def/tox-pyenv-redux\n',
    'author': 'un.def',
    'author_email': 'me@undef.im',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/un-def/pyenv-inspect',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
