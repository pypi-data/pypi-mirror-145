=========================
Isolated ``pip`` installs
=========================

Python packages are great. Virtual environments are great.
Installing tools from PyPI is awesome.
Installing multiple unrelated packages simultaneously in the one virtual environment can be chaos.
You might want ``docker-compose``, ``tox``, and ``aws`` all available globally,
but you don't want them stepping on each others toes inside the same virtual environment.
This is what ``pisque`` helps with!

``pisque`` will create a sequestered virtual environment,
install a package and its dependencies using ``pip``,
and symlink any installed executables into your ``~/.local/bin``.

.. code-block:: python

    $ pisque install tox
    Creating virtual environment ~/.local/virtual-environments/tox...
    Installing dependencies...
    Linking installed executables to ~/.local/bin
      * tox
    $ pisque install docker-compose
    Creating virtual environment ~/.local/virtual-environments/docker-compose...
    Installing dependencies...
    Linking installed executables to ~/.local/bin
      * docker-compose

Installing
----------

``pisque`` can be installed just like any other Python package.
You probably want to install it in its own isolated virtual environment though,
for exactly the same reasons that you want to use ``pisque`` in the first place!
The following bash snippet will install ``pisque`` to a scratch virtual environment,
then use ``pisque`` to install ``pisque``:

.. code-block:: console

    $ VIRTUAL_ENV=$( mktemp --directory --tmpdir "pisque-venv.XXXXXX" )
    $ python3 -m venv "$VIRTUAL_ENV"
    $ "$VIRTUAL_ENV/bin/pip" install pisque
    $ "$VIRTUAL_ENV/bin/pisque" install pisque
    $ rm -rf "$VIRTUAL_ENV"
