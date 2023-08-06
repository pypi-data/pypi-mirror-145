# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ps_typer',
 'ps_typer.assets.texts',
 'ps_typer.source_ui',
 'ps_typer.type_test',
 'ps_typer.type_test.components']

package_data = \
{'': ['*'], 'ps_typer': ['assets/*', 'assets/sounds/*', 'data/*']}

install_requires = \
['DateTime>=4.4,<5.0', 'PyQt5>=5.15.6,<6.0.0', 'pyqtgraph>=0.12.4,<0.13.0']

entry_points = \
{'console_scripts': ['ps-typer = ps_typer.main:main']}

setup_kwargs = {
    'name': 'ps-typer',
    'version': '0.1.5',
    'description': 'A Python program built on the PyQt5 GUI framework, used for practicing your typing skills and keeping track of your progress.',
    'long_description': "# ps-typer\n\n![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)\n![OSX](https://img.shields.io/badge/-OSX-black?logo=apple)\n![Windows](https://img.shields.io/badge/-Windows-blue?logo=windows)\n![Python](https://img.shields.io/badge/Python-v3.9%5E-green?logo=python)\n![Version](https://img.shields.io/github/v/tag/rolv-apneseth/ps-typer?label=version)\n[![PyPi](https://img.shields.io/pypi/v/ps-typer?label=pypi)](https://pypi.org/project/ps-typer/)\n![Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n![PS-Typer demo](https://user-images.githubusercontent.com/69486699/161395389-247c75fd-c2b6-4a63-bf03-258c5046b1be.png)\n\n## Description\n\nA Python program built on the PyQt5 GUI framework, used for practicing your typing skills and keeping track of your progress.\n\n## Index\n\n-   [Dependencies](#dependencies)\n-   [Installation](#installation)\n-   [Usage](#usage)\n-   [Modes](#modes)\n-   [W.P.M.](#wpm)\n-   [Statistics](#statistics)\n-   [License](#license)\n\n## Dependencies\n\n-   [Python3](https://www.python.org/downloads/) (v3.9 or later)\n    -   [DateTime](https://pypi.org/project/DateTime/)\n    -   [PyQt5](https://pypi.org/project/PyQt5/)\n    -   [PyQtGraph](https://pypi.org/project/pyqtgraph/)\n\n## Installation\n\nUsing `pip` (if you're on Windows, replace `python3` with just `python` down below):\n\n```bash\npython3 -m pip install ps-typer\n```\n\nThen, launch the program by running the command:\n\n```bash\nps-typer\n```\n\nNote that if the command does not work you may need to configure your system `PATH` variable (check out some Stack Overflow answers linked below).\n\n-   [Windows](https://stackoverflow.com/a/36160069/14316282)\n-   [Linux or Mac](https://stackoverflow.com/a/62823029/14316282)\n\n## Usage\n\n1. Select a [mode](#modes) from the dropdown menu (My recommendation is always `Random Text: Brown`)\n2. Click on begin and start typing! Characters typed correctly are highlighted green and characters typed incorrectly are highlighted red.\n3. When finished, a window will appear displaying your accuracy, average w.p.m and whether or not you set a daily or all-time high score.\n4. Check out the [Statistics](#statistics) section below\n\n## Modes\n\nSelect one of the following options to choose what you will be typing out:\n\n-   Common Phrases\n\n-   Facts\n\n-   Famous Literature Excerpts\n\n-   Famous Quotes\n\n-   Random Text Options\n    -   These 3 options are achieved using corpora from nltk, for which documentation can be found [here](https://www.nltk.org/book/ch02.html). The corpora included are:\n    1.  Brown, which is the first million-word electronic corpus of English.\n    2.  Gutenberg, which is a small selection of texts from the Project Gutenberg electronic text archive, which contains some 25,000 free electronic books, hosted [here](http://www.gutenberg.org/).\n    3.  Webtext, a collection of web text includes content from a Firefox discussion forum, conversations overheard in New York, the movie script of Pirates of the Carribean, personal advertisements, and wine reviews, for more informal text.\n    -   To reduce the number of dependencies, as well as the processing that needs to be done for formatting the text, the corpora are already processed into plain text files stored in the `assets/texts/` directory, along with the python script used to generate them.\n\n## W.P.M.\n\nYour typing speed is measured by your average wpm, multiplied by your accuracy.\n\nWpm is calculated as words per minute (w.p.m) using `(characters typed/5)/minutes` This gives a more fair w.p.m calculation since longer words would be worth more than short words. This figure is then multiplied by your accuracy percentage.\n\nAccuracy is taken into account to incentivise you to type all the text out correctly and not enforce bad habits.\n\n## Statistics\n\nThe program will save all of your daily high scores and keep track of your all-time highscore. This data is then visualised in the `Statistics` window using a graph of wpm over time so you can get a sense of how you're progressing.\n\nFrom here you can also reset your highscores if you so wish.\n\n**Please note:** All the (very limited) data this program stores can be found in the `ps_typer/data/` directory\n\n## License\n\n[MIT](https://github.com/Rolv-Apneseth/ps-typer/blob/master/LICENSE)\n",
    'author': 'Rolv-Apneseth',
    'author_email': 'rolv.apneseth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rolv-Apneseth/ps-typer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0.0',
}


setup(**setup_kwargs)
