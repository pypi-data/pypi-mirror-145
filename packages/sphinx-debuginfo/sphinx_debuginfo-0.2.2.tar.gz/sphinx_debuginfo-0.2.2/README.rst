#################
sphinx-debuginfo
#################

.. start short_desc

**A Sphinx extension to include debugging information in the output.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/sphinx-toolbox/sphinx-debuginfo/workflows/Linux/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/sphinx-toolbox/sphinx-debuginfo/workflows/Windows/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/sphinx-toolbox/sphinx-debuginfo/workflows/macOS/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/sphinx-toolbox/sphinx-debuginfo/workflows/Flake8/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/sphinx-toolbox/sphinx-debuginfo/workflows/mypy/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.herokuapp.com/github/sphinx-toolbox/sphinx-debuginfo/badge.svg
	:target: https://dependency-dash.herokuapp.com/github/sphinx-toolbox/sphinx-debuginfo/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/sphinx-toolbox/sphinx-debuginfo/master?logo=coveralls
	:target: https://coveralls.io/github/sphinx-toolbox/sphinx-debuginfo?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/sphinx-toolbox/sphinx-debuginfo?logo=codefactor
	:target: https://www.codefactor.io/repository/github/sphinx-toolbox/sphinx-debuginfo
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/sphinx-debuginfo
	:target: https://pypi.org/project/sphinx-debuginfo/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sphinx-debuginfo?logo=python&logoColor=white
	:target: https://pypi.org/project/sphinx-debuginfo/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sphinx-debuginfo
	:target: https://pypi.org/project/sphinx-debuginfo/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/sphinx-debuginfo
	:target: https://pypi.org/project/sphinx-debuginfo/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/sphinx-toolbox/sphinx-debuginfo
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/sphinx-toolbox/sphinx-debuginfo
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/sphinx-toolbox/sphinx-debuginfo/v0.2.2
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/sphinx-toolbox/sphinx-debuginfo
	:target: https://github.com/sphinx-toolbox/sphinx-debuginfo/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/sphinx-debuginfo
	:target: https://pypi.org/project/sphinx-debuginfo/
	:alt: PyPI - Downloads

.. end shields

See an example of the output in the documentation for
`sphinx-toolbox <https://sphinx-toolbox.readthedocs.io/en/latest/_debug/>`_.

Installation
--------------

.. start installation

``sphinx-debuginfo`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install sphinx-debuginfo

.. end installation
