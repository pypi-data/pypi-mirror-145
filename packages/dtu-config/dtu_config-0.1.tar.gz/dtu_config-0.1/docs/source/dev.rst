.. _developers_guide:

Installation
============
To edit the project, clone the `repository <https://gitlab-internal.windenergy.dtu.dk/ram/software/project-config>`_


You can then install the developer tools and the package in editable mode by running

.. code-block:: sh

	pip install -e .[dev]

Building packages by hand
==========================

.. note:: This should rarely be necessary, let CI do the job

.. code-block:: sh

	pip install build
	pip -m build

	conda install boa conda-verify
	export VERSION=`grep 'version = ' dtu_conf/_version.py | cut -d \' -f 2`
	conda mambabuild --output-folder dist/conda ./recipe
