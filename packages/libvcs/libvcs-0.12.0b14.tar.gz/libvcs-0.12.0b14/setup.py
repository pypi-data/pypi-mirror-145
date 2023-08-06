# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libvcs', 'libvcs.states']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libvcs',
    'version': '0.12.0b14',
    'description': 'vcs abstraction layer',
    'long_description': "# `libvcs` &middot; [![Python Package](https://img.shields.io/pypi/v/libvcs.svg)](https://pypi.org/project/libvcs/) [![License](https://img.shields.io/github/license/vcs-python/libvcs.svg)](https://github.com/vcs-python/libvcs/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/vcs-python/libvcs/branch/master/graph/badge.svg)](https://codecov.io/gh/vcs-python/libvcs)\n\nlibvcs is an abstraction layer for vcs systems. powers\n[vcspull](https://www.github.com/vcs-python/vcspull/).\n\n## Setup\n\n```console\n$ pip install --user libvcs\n```\n\nOpen up python:\n\n```console\n$ python\n\n// or for nice autocomplete and syntax highlighting\n$ pip install --user ptpython\n$ ptpython\n```\n\n## Usage\n\nCreate a [Repo](https://libvcs.git-pull.com/api.html#creating-a-repo-object) object of the project\nto inspect / checkout / update:\n\n```python\n>>> from libvcs.shortcuts import create_repo_from_pip_url, create_repo\n\n# repo is an object representation of a vcs repository.\n>>> r = create_repo(url='https://www.github.com/vcs-python/libtmux',\n...                 vcs='git',\n...                 repo_dir='/tmp/libtmux')\n\n# or via pip-style URL\n>>> r = create_repo_from_pip_url(\n...         pip_url='git+https://www.github.com/vcs-python/libtmux',\n...         repo_dir='/tmp/libtmux')\n```\n\nUpdate / clone repo:\n\n```python\n# it may or may not be checked out/cloned on the system yet\n>>> r.update_repo()\n```\n\nGet revision:\n\n```python\n>>> r.get_revision()\nu'5c227e6ab4aab44bf097da2e088b0ff947370ab8'\n```\n\n## Donations\n\nYour donations fund development of new features, testing and support. Your money will go directly to\nmaintenance and development of the project. If you are an individual, feel free to give whatever\nfeels right for the value you get out of the project.\n\nSee donation options at <https://www.git-pull.com/support.html>.\n\n## More information\n\n- Python support: 3.9+, pypy\n- VCS supported: git(1), svn(1), hg(1)\n- Source: <https://github.com/vcs-python/libvcs>\n- Docs: <https://libvcs.git-pull.com>\n- Changelog: <https://libvcs.git-pull.com/history.html>\n- API: <https://libvcs.git-pull.com/api.html>\n- Issues: <https://github.com/vcs-python/libvcs/issues>\n- Test Coverage: <https://codecov.io/gh/vcs-python/libvcs>\n- pypi: <https://pypi.python.org/pypi/libvcs>\n- Open Hub: <https://www.openhub.net/p/libvcs>\n- License: [MIT](https://opensource.org/licenses/MIT).\n\n[![Docs](https://github.com/vcs-python/libvcs/workflows/docs/badge.svg)](https://libvcs.git-pull.com/)\n[![Build Status](https://github.com/vcs-python/libvcs/workflows/tests/badge.svg)](https://github.com/vcs-python/libvcs/actions?query=workflow%3A%22tests%22)\n",
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/vcs-python/libvcs/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
