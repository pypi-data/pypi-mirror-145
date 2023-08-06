# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_tox_pyenv_redux']

package_data = \
{'': ['*']}

install_requires = \
['pyenv-inspect>=0.2,<0.3', 'tox']

entry_points = \
{'tox': ['pyenv-redux = _tox_pyenv_redux.plugin']}

setup_kwargs = {
    'name': 'tox-pyenv-redux',
    'version': '0.1.0',
    'description': 'A tox plugin using pyenv to find Python executables',
    'long_description': '# tox-pyenv-redux\n\nA [tox][tox] plugin using [pyenv][pyenv] to find Python executables\n\n\n[tox]: https://tox.wiki/\n[pyenv]: https://github.com/pyenv/pyenv\n',
    'author': 'un.def',
    'author_email': 'me@undef.im',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/un-def/tox-pyenv-redux',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
