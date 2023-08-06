# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['antsibull_core',
 'antsibull_core.schemas',
 'antsibull_core.utils',
 'antsibull_core.vendored',
 'tests',
 'tests.functional',
 'tests.units']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'aiofiles',
 'aiohttp>=3.0.0',
 'packaging>=20.0',
 'perky',
 'pydantic',
 'semantic_version',
 'sh',
 'twiggy>=0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 ':python_version >= "3.6" and python_version < "3.7"': ['aiocontextvars']}

setup_kwargs = {
    'name': 'antsibull-core',
    'version': '0.1.0',
    'description': 'Tools for building the Ansible Distribution',
    'long_description': '# antsibull-core -- Library for Ansible Build Scripts\n[![Python linting badge](https://github.com/ansible-community/antsibull-core/workflows/Python%20linting/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-core/actions?query=workflow%3A%22Python+linting%22+branch%3Amain)\n[![Python testing badge](https://github.com/ansible-community/antsibull-core/workflows/Python%20testing/badge.svg?event=push&branch=main)](https://github.com/ansible-community/antsibull-core/actions?query=workflow%3A%22Python+testing%22+branch%3Amain)\n[![Codecov badge](https://img.shields.io/codecov/c/github/ansible-community/antsibull-core)](https://codecov.io/gh/ansible-community/antsibull-core)\n\nLibrary needed for tooling for building various things related to Ansible.\n\nYou can find a list of changes in [the antsibull-core changelog](./CHANGELOG.rst).\n\nUnless otherwise noted in the code, it is licensed under the terms of the GNU\nGeneral Public License v3 or, at your option, later.\n\nantsibull-core is covered by the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).\n\n## Creating a new release:\n\nIf you want to create a new release::\n\n    vim changelogs/fragment/$VERSION_NUMBER.yml  # create \'release_summary:\' fragment\n    antsibull-changelog release --version $VERSION_NUMBER\n    git add CHANGELOG.rst changelogs\n    git commit -m "Release $VERSION_NUMBER."\n    poetry build\n    poetry publish  # Uploads to pypi.  Be sure you really want to do this\n\n    git tag $VERSION_NUMBER\n    git push --tags\n    vim pyproject.toml    # Bump the version number\n    git commit -m \'Update the version number for the next release\' pyproject.toml\n    git push\n',
    'author': 'Toshio Kuratomi',
    'author_email': 'a.badger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ansible-community/antsibull-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
