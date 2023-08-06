# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pisque']
install_requires = \
['ConfigArgParse[yaml]>=1.5.3,<2.0.0']

entry_points = \
{'console_scripts': ['pisque = pisque:run']}

setup_kwargs = {
    'name': 'pisque',
    'version': '0.1.0',
    'description': 'Install Python packages in an isolated virtual environment',
    'long_description': '=========================\nIsolated ``pip`` installs\n=========================\n\nPython packages are great. Virtual environments are great.\nInstalling tools from PyPI is awesome.\nInstalling multiple unrelated packages simultaneously in the one virtual environment can be chaos.\nYou might want ``docker-compose``, ``tox``, and ``aws`` all available globally,\nbut you don\'t want them stepping on each others toes inside the same virtual environment.\nThis is what ``pisque`` helps with!\n\n``pisque`` will create a sequestered virtual environment,\ninstall a package and its dependencies using ``pip``,\nand symlink any installed executables into your ``~/.local/bin``.\n\n.. code-block:: console\n\n    $ pisque install tox\n    Creating virtual environment ~/.local/share/pisque/environments/tox...\n    Installing dependencies...\n    Linking installed executables to ~/.local/bin\n      * tox\n    $ pisque install docker-compose\n    Creating virtual environment ~/.local/share/pisque/environments/docker-compose...\n    Installing dependencies...\n    Linking installed executables to ~/.local/bin\n      * docker-compose\n\nInstalling\n----------\n\n``pisque`` can be installed just like any other Python package.\nYou probably want to install it in its own isolated virtual environment though,\nfor exactly the same reasons that you want to use ``pisque`` in the first place!\nThe following bash snippet will install ``pisque`` to a scratch virtual environment,\nthen use ``pisque`` to install ``pisque``:\n\n.. code-block:: console\n\n    $ VIRTUAL_ENV=$( mktemp --directory --tmpdir "pisque-venv.XXXXXX" )\n    $ python3 -m venv "$VIRTUAL_ENV"\n    $ "$VIRTUAL_ENV/bin/pip" install pisque\n    $ "$VIRTUAL_ENV/bin/pisque" install pisque\n    $ rm -rf "$VIRTUAL_ENV"\n',
    'author': 'Tim Heap',
    'author_email': 'tim@timheap.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
