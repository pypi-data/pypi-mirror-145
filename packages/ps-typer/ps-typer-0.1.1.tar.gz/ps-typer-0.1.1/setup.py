# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ps_typer',
 'ps_typer.assets.texts',
 'ps_typer.source_ui',
 'ps_typer.type_test',
 'ps_typer.type_test.components']

package_data = \
{'': ['*'], 'ps_typer': ['assets/*', 'assets/sounds/*', 'data/.gitignore']}

install_requires = \
['DateTime>=4.4,<5.0', 'PyQt5>=5.15.6,<6.0.0', 'pyqtgraph>=0.12.4,<0.13.0']

entry_points = \
{'console_scripts': ['ps-typer = ps_typer.main:main']}

setup_kwargs = {
    'name': 'ps-typer',
    'version': '0.1.1',
    'description': 'A Python program with a PyQt5 UI used for practicing your typing skills and keeping track of your progress',
    'long_description': "# ps-typer\n\n![PS-Typer](https://user-images.githubusercontent.com/69486699/161395389-247c75fd-c2b6-4a63-bf03-258c5046b1be.png)\n\n\n## Description\n\nA Python program built on the PyQt5 GUI framework, used for practicing your typing skills and keeping track of your progress.\n\n## Index\n\n- [Dependencies](#dependencies)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Modes](#modes)\n- [W.P.M.](#wpm)\n- [Statistics](#statistics)\n- [License](#license)\n\n## Dependencies\n\n- [Python3](https://www.python.org/downloads/) (v3.6 or later)\n- All Python packages required are listed in `requirements.txt` and are installed automatically with the default installation process (including [PyQt5](https://pypi.org/project/PyQt5/) and [PyQtGraph](https://pypi.org/project/pyqtgraph/))\n\n## Installation\n\nTo download this program, click on `Code` at the top right of this page, then download as a zip file. You can unzip using your preferred program.\n\nAlternatively, clone the repository using `git`:\n\n```bash\ngit clone https://github.com/Rolv-Apneseth/ps-typer.git\n```\n\n### Linux\n\nNavigate to the project's home directory and run the command:\n\n```bash\nsudo make install\n```\n\n- This will place a script for easy launching at `/usr/local/ps-typer`\n\nTo launch the program, run the command:\n\n```bash\nps-typer\n```\n\n- This runs the `run_program.sh` script (located in the `bin` directory) which will create a virtual envirionment, install all required Python packages and then launch the program.\n\n### Windows\n\nNavigate to the project's `bin` directory and double click on `run_program.bat`\n\n- This will create a virtual envirionment, install all required Python packages and then launch the program.\n\n### Manual\n\nNavigate to the project's home directory and run the command:\n\n```bash\npython3 -m pip install -r requirements.txt\n```\n\nTo launch the program, navigate into the `ps-typer` directory and run the command:\n\n```bash\npython3 main.py\n```\n\nWindows users, replace `python3` with just `python` in the above commands\n\n## Usage\n\n1. Select a mode from the dropdown menu (Default on first start is Common Phrases)\n2. Click on begin and start typing! Characters typed correctly are highlighted green and characters typed incorrectly are highlighted red.\n3. When finished, a window will appear displaying your accuracy, average w.p.m and whether or not you set a daily or all-time high score.\n   - Note: The high scores are stored in the assets folder in `highscores.pkl` and `backup_highscores.pkl` and can be deleted if you want to reset your high score.\n     - There are however GUI options for resetting high scores in the Statistics window\n\n## Modes\n\nSelect one of the following options to choose what you will be typing out:\n\n- Common Phrases\n\n- Facts\n\n- Famous Literature Excerpts\n\n- Famous Quotes\n\n- Random Text Options\n  - These 3 options are achieved using corpora from nltk, for which documentation can be found [here](https://www.nltk.org/book/ch02.html). The corpora included are:\n  1.  Brown, which is the first million-word electronic corpus of English.\n  2.  Gutenberg, which is a small selection of texts from the Project Gutenberg electronic text archive, which contains some 25,000 free electronic books, hosted [here](http://www.gutenberg.org/).\n  3.  Webtext, a collection of web text includes content from a Firefox discussion forum, conversations overheard in New York, the movie script of Pirates of the Carribean, personal advertisements, and wine reviews, for more informal text.\n  - To reduce the number of dependencies, as well as the processing that needs to be done for formatting the text, the corpora are already processed into plain text files stored in the `assets/texts/` directory, along with the python script used to generate them.\n\n## W.P.M.\n\nYour typing speed is measured by your average wpm, multiplied by your accuracy.\n\nWpm is calculated as words per minute (w.p.m) using `(characters typed/5)/minutes` This gives a more fair w.p.m calculation since longer words would be worth more than short words. This figure is then multiplied by your accuracy percentage.\n\nAccuracy is taken into account to incentivise you to type all the text out correctly and not enforce bad habits.\n\n## Statistics\n\nHigh scores can be set both daily or as an all-time high score. Both values are displayed in the main menu and saved for future sessions.\n\nThe program will save all of your daily high scores. This data is then visualised in the statistics window using a graph of wpm over time so you can get a sense of how you're progressing.\n\n## License\n\n[MIT](https://github.com/Rolv-Apneseth/ps-typer/blob/master/LICENSE)\n",
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
