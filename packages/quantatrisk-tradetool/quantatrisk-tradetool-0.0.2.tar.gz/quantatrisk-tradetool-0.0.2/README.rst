========
Overview
========

Internal tooling

* Free software: BSD 2-Clause License

Installation
============

::

    pip install quantatrisk-tradetool

You can also install the in-development version with::

    pip install git+ssh://git@quantatrisk_tradetool/pablomasior/python-quantatrisk_tradetool.git@main

Documentation
=============


https://python-quantatrisk_tradetool.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
