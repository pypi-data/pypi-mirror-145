.. -*- mode: rst -*-

.. _statsmodels: https://www.statsmodels.org/stable/

.. _scikit-learn: http://scikit-learn.org/stable/

.. _imbalanced-learn: http://imbalanced-learn.org/en/stable/

|ReadTheDocs|_ |PythonVersion|_ |Pypi|_ |Black|_

.. |ReadTheDocs| image:: https://readthedocs.org/projects/research-learn/badge/?version=latest
.. _ReadTheDocs: https://research-learn.readthedocs.io/en/latest/?badge=latest

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/research-learn.svg
.. _PythonVersion: https://img.shields.io/pypi/pyversions/research-learn.svg

.. |Pypi| image:: https://badge.fury.io/py/research-learn.svg
.. _Pypi: https://badge.fury.io/py/research-learn

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
.. _Black: https://github.com/ambv/black

==============
research-learn
==============

Toolbox to simplify the design, execution and analysis of machine learning
experiments. It based on  statsmodels_, scikit-learn_ and imbalanced-learn_.

Documentation
-------------

Installation documentation, API documentation, and examples can be found on the
documentation_.

.. _documentation: https://research-learn.readthedocs.io/en/latest/

Dependencies
------------

research-learn is tested to work under Python 3.6+. The dependencies are the
following:

- numpy(>=1.1)
- statsmodels(>=0.9.0)
- scikit-learn(>=0.22)
- imbalanced-learn(>=0.6.0)

Additionally, to run the examples, you need matplotlib(>=2.0.0) and
pandas(>=0.22).

Installation
------------

research-learn is currently available on the PyPi's repository and you can
install it via `pip`::

  pip install -U research-learn

The package is released also in Anaconda Cloud platform::

  conda install -c gdouzas research-learn

If you prefer, you can clone it and run the setup.py file. Use the following
commands to get a copy from GitHub and install all dependencies::

  git clone https://github.com/georgedouzas/research-learn.git
  cd research-learn
  pip install .

Or install using pip and GitHub::

  pip install -U git+https://github.com/georgedouzas/research-learn.git

Testing
-------

After installation, you can use `pytest` to run the test suite::

  make test
