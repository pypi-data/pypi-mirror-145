# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['otf']

package_data = \
{'': ['*']}

extras_require = \
{'dev-tools': ['pytest-watch', 'sphinx-autobuild', 'grip']}

setup_kwargs = {
    'name': 'otf',
    'version': '0.1.0a1',
    'description': 'A python framework for on-the-fly distributed workflows',
    'long_description': 'On-the-fly distributed python workflows\n=======================================\n\n|PyPI| |PyPI - Python Version| |License: CC0-1.0| |Tests| |codecov|\n|Documentation Status|\n\nOTF is a framework to programatically write, run and debug workflows.\n\nInstalling\n----------\n\nOTF is currently in pre-alpha. If you really want to play with it you\ncan install the latest build via:\n\n.. code:: bash\n\n   $ pip install -i https://test.pypi.org/simple/ otf\n\n`Contributing to this project <CONTRIBUTING.rst>`__\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/otf.svg\n   :target: https://pypi.org/project/otf/\n.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/otf\n.. |License: CC0-1.0| image:: https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg\n   :target: http://creativecommons.org/publicdomain/zero/1.0/\n.. |Tests| image:: https://github.com/till-varoquaux/otf/actions/workflows/ci.yml/badge.svg?branch=main\n   :target: https://github.com/till-varoquaux/otf/actions/workflows/ci.yml\n.. |codecov| image:: https://codecov.io/gh/till-varoquaux/otf/branch/main/graph/badge.svg?token=ahhI117oFg\n   :target: https://codecov.io/gh/till-varoquaux/otf\n.. |Documentation Status| image:: https://readthedocs.org/projects/otf/badge/?version=latest\n   :target: https://otf.readthedocs.io/en/latest/?badge=latest\n',
    'author': 'Till Varoquaux',
    'author_email': 'till.varoquaux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/till-varoquaux/otf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
