# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readmetester']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.8.1,<3.0.0',
 'object-colors>=2.0.0,<3.0.0',
 'pyproject-parser>=0.4.3,<0.5.0',
 'restructuredtext-lint>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['readmetester = readmetester:main']}

setup_kwargs = {
    'name': 'readmetester',
    'version': '2.2.0',
    'description': 'Parse, test, and assert RST code-blocks',
    'long_description': 'READMETester\n============\n.. image:: https://github.com/jshwi/readmetester/workflows/build/badge.svg\n    :target: https://github.com/jshwi/readmetester/workflows/build/badge.svg\n    :alt: build\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/readmetester\n    :target: https://img.shields.io/pypi/v/readmetester\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/readmetester/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/readmetester\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nParse and test README.rst Python code-blocks\n\n**Installation**\n\n.. code-block:: console\n\n    $ pip install readmetester\n..\n\nCode blocks need to begin with\n\n``.. code-block:: python``\n\nfollowed by a blank line\n\nEnd a code block with another blank line\n\n**Usage**\n\n``readmetester [-h] file``\n\nIf a README.rst file is present in the current working directory it will be used if no arguments are provided\n\n.. code-block:: console\n\n    $ readmetester README.rst\n..\n\n**Documenting**\n\nDocumented code needs to be indented\n\nPython code begins with ``">>> "``\n\n.. note::\n\n    The length of the string is 4 including the whitespace at the end\n..\n\nExpected output can be single quoted or unquoted (no double quotes)\n\n.. code-block:: RST\n\n    .. code-block:: python\n\n        >>> print("Hello, world!")\n        \'Hello, world!\'\n\nContinuation lines begin with ``"... "``\n\n.. code-block:: RST\n\n    .. code-block:: python\n\n        >>> n = [\n        ...     "zero",\n        ...     "one",\n        ...     "two",\n        ... ]\n        >>> for c, i in enumerate(n):\n        ...     print(c, i)\n        0 zero\n        1 one\n        2 two\n\n\nStyles can be configured in a pyproject.toml file\n\n.. code-block:: toml\n\n    [tool.readmetester]\n    style = "monokai"\n\n\nUsing `readmetester` API\n\n.. code-block:: python\n\n    >>> import readmetester\n    >>> readmetester.main()\n    \'recursive exec not implemented\'\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
