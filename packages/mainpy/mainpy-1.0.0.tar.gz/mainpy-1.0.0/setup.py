# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mainpy']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.10"': ['typing_extensions>=4.1,<5.0']}

setup_kwargs = {
    'name': 'mainpy',
    'version': '1.0.0',
    'description': "Simplify your project's main entrypoint definition with @main",
    'long_description': "# `@main`.py\n\n-----\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/mainpy.svg)](https://pypi.python.org/pypi/mainpy/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mainpy.svg)](https://pypi.python.org/pypi/mainpy/)\n[![PyPI license](https://img.shields.io/pypi/l/mainpy.svg)](https://pypi.python.org/pypi/mainpy/)\n\n-----\n\n## Installation\n\n```bash\npip install mainpy\n```\n\n*requires python > 3.7*\n\n## Usage\n\n```python\nfrom mainpy import main\n\n@main\ndef app(): ...\n```\n\nAsync functions will be automatically wrapped in `asyncio.run`.\n\n```python\n@main\nasync def async_app(): ...\n```\n\n# Automatic uvloop usage\n\nIf you have [uvloop](https://github.com/MagicStack/uvloop) installed, mainpy\nwill automatically call `uvloop.install()` before running your async main \nfunction. This can be disabled by setting `use_uvloop=False`, e.g.:\n\n```python\n@main(use_uvloop=False)\nasync def app(): ...\n```\n\n## Debug mode\n\nOptionally, python's [development mode](https://docs.python.org/3/library/devmode.html) \ncan be emulated by setting `debug=True` in `@main`. This will enable the\n[faulthandler](https://docs.python.org/3/library/faulthandler.html#faulthandler.enable), \nconfigure the [`warnings`](https://docs.python.org/3/library/warnings.html) \nfilter to display all warnings, and activate the\n[asyncio debug mode](https://docs.python.org/3/library/asyncio-dev.html#asyncio-debug-mode):\n\n```python\n@main(debug=True)\ndef app(): ...\n```\n",
    'author': 'Joren Hammudoglu',
    'author_email': 'jhammudoglu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorenham/mainpy',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
