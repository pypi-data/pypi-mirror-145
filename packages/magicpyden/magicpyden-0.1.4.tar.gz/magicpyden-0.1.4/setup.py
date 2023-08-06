# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magicpyden']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0',
 'inflection>=0.5.1,<0.6.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'magicpyden',
    'version': '0.1.4',
    'description': 'Async Python API wrapper for MagicEden',
    'long_description': '# MagicPyden\n\n[![Github Issues](https://img.shields.io/github/issues/ChristianPerez34/magicpyden?logo=github&style=for-the-badge)](https://github.com/ChristianPerez34/magicpyden/issues)\n[![Codacy Badge](https://img.shields.io/codacy/grade/12257657689e48369b7e91b215dcb14a?logo=codacy&style=for-the-badge)](https://www.codacy.com/gh/ChristianPerez34/magicpyden/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ChristianPerez34/magicpyden&amp;utm_campaign=Badge_Grade)\n[![Github Top Language](https://img.shields.io/github/languages/top/Stonks-Luma-Liberty/Crepitus?logo=python&style=for-the-badge)](https://www.python.org)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg?style=for-the-badge)](https://github.com/wemake-services/wemake-python-styleguide)\n\nAsynchronous API wrapper for the MagicEden API\n\n## Installation\n\nPyPi\n\n```bash\n  pip install magicpyden\n```\n\nPoetry\n\n```bash\n  poetry add magicpyden\n```\n\nFrom source\n\n```bash\n  git clone https://github.com/ChristianPerez34/magicpyden.git\n  cd magicpyden\n  python setup.py install\n```\n\n## Usage/Examples\n\n[Official Documentation](https://api.magiceden.dev)\n\n```python\nfrom magicpyden import MagicEdenApi\n\n# Assuming inside async function/method\nasync with MagicEdenApi() as api:\n    collection_stats = await api.get_collection_stats(collection_name="degods")\n```\n',
    'author': 'Christian Pérez Villanueva',
    'author_email': 'perez.villanueva.christian34@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
