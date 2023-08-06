# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fafi']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0', 'click>=8.0,<9.0', 'newspaper3k>=0.2,<0.3']

entry_points = \
{'console_scripts': ['fafi = fafi.fafi:cli']}

setup_kwargs = {
    'name': 'fafi',
    'version': '0.2.1',
    'description': 'CLI for indexing Firefox bookmarks.',
    'long_description': "\nFafi\n====\n\nSearch Firefox bookmark contents, with this commandline client. Fafi extracts the content of the bookmarks and stores them into a searchable SQLite database.\n\nThings it does:\n\n\n* Detects your places database from the Firefox profile folder. (support for picking a profile from multiple profiles)\n* Extract main text content from all bookmarks into ``<user_data_dir>/fafi/data.sqlite``.\n* Skips .local and .test domains.\n* Skips pages that are already indexed.\n* Search results are ranked by relevance and displayed with snippets.\n\nURLs are stored together with the main page context as determined by `Newspaper <https://github.com/codelucas/newspaper>`_.\n\nUsers\n-----\n\n.. code-block::\n\n   pipx install fafi\n   fafi --help\n   fafi index\n   fafi search 'linux'\n\nDevelopers\n----------\n\n.. code-block::\n\n   # Install project requirements.\n   poetry install\n\n   # Log in to a python shell\n   poetry shell\n\n   # Make faff executable\n   chmod +x fafi.py\n\n   # Help on commands\n   ./fafi.py --help\n   \n   # Index bookmarks\n   ./fafi.py index\n\n   # Search for linux\n   ./fafi.py search 'linux'\n\n\n.. image:: https://user-images.githubusercontent.com/594871/76201330-ffcba880-61ea-11ea-9fdd-cc32a90deecd.png\n   :target: https://user-images.githubusercontent.com/594871/76201330-ffcba880-61ea-11ea-9fdd-cc32a90deecd.png\n   :alt: search query\n\n",
    'author': 'Sander van Dragt',
    'author_email': 'sander@vandragt.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
