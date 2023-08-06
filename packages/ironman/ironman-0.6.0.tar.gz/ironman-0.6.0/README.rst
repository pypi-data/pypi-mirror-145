Ironman
=======

|PyPI version| |Docs|

|Build Status| |codecov| |Code Health|

What is Ironman?
----------------

Ironman is a general purpose software toolbox to be run on L1Calo
hardware with embedded processors (SoCs).

Look how easy it is to use

.. code:: python

    >>> import ironman
    >>> # Get your stuff done
    >>> ironman.engage()

Features
--------

-  Be awesome
-  Make things faster

Getting Started
---------------

Installing
~~~~~~~~~~

Install ironman by running

::

    pip install ironman

Developing
~~~~~~~~~~

If it is your first time...

::

    git clone git@github.com:kratsg/ironman
    cd ironman && mkvirtualenv ironman
    pip install -r requirements.txt

and then afterwards...

::

    workon ironman
    python setup.py develop
    ... do work here ...
    pip uninstall ironman

Testing
^^^^^^^

::

    tox

or with

::

    py.test

Contributing
~~~~~~~~~~~~

-  `Issue Tracker <https://github.com/kratsg/ironman/issues>`__
-  `Source Code <https://github.com/kratsg/ironman>`__

Support
~~~~~~~

If you are having issues, let us know.

Releasing
~~~~~~~~~

1. Do some work on your package (i.e. fix bugs, add features, etc)
2. Make sure the tests pass. Run ``pytest``.
3. Update the ``__version__`` number via ``bump2version``.
4. Push to the default branch.

Tutorial
--------

Since we will be predominantly using Twisted within the Zynq to manage
the Reactor workflow ("callbacks"), I suggest reading through `this
tutorial <http://krondo.com/?page_id=1327>`__ on your own time to get up
to speed on how it works and some details of sockets.

I'm following the guide based on ``sandman``
`here <https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/>`__

To Do
-----

-  split udp and tcp into different, separate protocols:
   http://stackoverflow.com/questions/33224142/twisted-protocol-that-simultaneously-handles-tcp-and-udp-at-once

Ideas
-----

-  make it like twisted.web - we build Request objects which need to
   find Resource objects that provide actions (maybe too complicated,
   try and simplify?)
   `link <http://twistedmatrix.com/trac/browser/trunk/twisted/web>`__

.. |PyPI version| image:: https://badge.fury.io/py/ironman.svg
   :target: https://badge.fury.io/py/ironman
.. |Docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
   :target: http://ironman.readthedocs.org/en/latest/intro.html
.. |Build Status| image:: https://travis-ci.org/kratsg/ironman.svg?branch=master
   :target: https://travis-ci.org/kratsg/ironman
.. |codecov| image:: https://codecov.io/gh/kratsg/ironman/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/kratsg/ironman
.. |Code Health| image:: https://landscape.io/github/kratsg/ironman/master/landscape.svg?style=flat
   :target: https://landscape.io/github/kratsg/ironman/master
