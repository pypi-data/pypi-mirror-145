# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grab_convert_from_libgen']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0,<5.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'grab-convert-from-libgen',
    'version': '2.0.0',
    'description': 'An easy API for searching and downloading books from Libgen.',
    'long_description': '# grab-convert-from-libgen\nAn easy API for searching and downloading books from Libgen.\n\n## Before Installing\n\n**Be sure that you have installed Calibre and have added the necessary `ebook-convert` command to your path!**\n\n[calibre](https://calibre-ebook.com/) is "a powerful and easy to use e-book manager". It\'s also free, open-source, and super easy to use.\n\nYou can install an calibre executable, through MacOS Homebrew, compile from source... pick your poison. They only thing you need to be sure of \nis the command `ebook-convert` is in your PATH.\n\n## Install\n\nInstall by \n\n```\npip install grab-convert-from-libgen\n```\n\n## Quickstart\n\nThe example below shows to grab the first book returned from a search and save it to your current working directory as a pdf.\n\n```python\nfrom grab_from_libgen import LibgenSearch\n\nres = LibgenSearch(\'sci-tech\', q=\'test\')\n\nres.first(convert_to=\'pdf\')\n```\n\nThis is an example the gets and downloads a book that matches a given title.\n\n```python\nfrom grab_from_libgen import LibgenSearch\n\nres = LibgenSearch(\'fiction\', q=\'test\')\n\nres.get(title=\'a title\', save_to=\'.\')\n```\n\nYou must specify a `topic` when creating a search instance. Choices are `fiction` or `sci-tech`.\n\n## Documentation\n\nOnly search parameters marked as required are needed when searching.\n\n### Libgen Non-fiction/Sci-tech\n#### Search Parameters\n\n`q`: The search query (required)\n\n`sort`: Sort results. Choices are `def` (default), `id`, `title`, `author`, `publisher`, `year`\n\n`sortmode`: Ascending or decending. Choices are `ASC` or `DESC`\n\n`column`: The column to search against. Choices are `def` (default), `title`, `author`, `publisher`, `year`, `series`, `ISBN`, `Language`, or `md5`.\n\n`phrase`: Search with mask (word*). Choices are `0` or `1`.\n\n`res`: Results per page. Choices are `25`, `50`, or `100`.\n\n`page`: Page number\n\n### Libgen Fiction\n#### Search Parameters\n\n`q`: The search query (required)\n\n`criteria`: The column to search against. Choices are `title`, `authors`, or `series`.\n\n`language`: Language code\n\n`format`: File format\n\n`wildcard`: Wildcarded words (word*). Set to `1`.\n\n`page`: Page number\n\n### LibgenSearch\n#### get_results\n\n`get_results(self) -> OrderedDict`\n\nCaches and returns results based on the search parameters the `LibgenSearch` objects was initialized with. Results are ordered\nin the same order as they would be displayed on libgen itself with the book\'s id serving as the key.\n\n#### first\n\n`first(save_to: str = None, convert_to: str = None) -> Dict`\n\nReturns a the first book (as a dictionary) from the cached or obtained results.\n\n#### get\n\n`get(save_to: str = None, convert_to: str = None, **filters) -> Dict`\n\nReturns the first book (as a dictionary) from the cached or obtained results that match the given filter parameters.\n\nThe filter parameters must be pulled from the keys that the book dictionary object returns.\n',
    'author': 'Will Meyers',
    'author_email': 'will@willmeyers.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willmeyers/grab-convert-from-libgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
