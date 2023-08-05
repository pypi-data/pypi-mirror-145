# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['book_queue']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.34,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['book-queue = book_queue.main:app']}

setup_kwargs = {
    'name': 'book-queue',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Book-Queue\n\nSimple tool to manage a collection of in-progress books to get a varied reading intake, written in Python with [Poetry](https://python-poetry.org/), [Typer](https://typer.tiangolo.com/), and [SQLAlchemy](https://www.sqlalchemy.org/).\n\n## Features\n\n- Manage books in collection\n- Prioritise queue based on importance and time since last access\n- Read books (by default in [Zathura](https://pwmt.org/projects/zathura/))\n\n```\n> book-queue read\n| No  | File                                                                                             | Acc Prio    | Prio | Modified                   |\n| --- | ------------------------------------------------------------------------------------------------ | ----------- | ---- | -------------------------- |\n| 1   | Introduction_to_algorithms-3rd Edition.pdf                                                       | 0.0107284   | 50   | 2022-04-01 15:00:57.944001 |\n| 2   | Adrian Ostrowski_ Piotr Gaczkowski - Software Architecture with C++-Packt Publishing (2021).epub | 0.000870491 | 10   | 2022-04-01 15:01:08.961704 |\n\n```\n\n',
    'author': 'ShaddyDC',
    'author_email': 'shaddy@shaddy.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
