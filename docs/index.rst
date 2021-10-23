The CI python template
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

The example project for to craete CI tools for python module
The command-line interface prints random tags to your console,
using ConnectedBrewery.


Installation
------------

To install the Hypermodern Python project,
run this command in your terminal:

.. code-block:: console

   $ pip install python-ci-template


Usage
-----

CI Python's usage looks like:

.. code-block:: console

   $ my-script [OPTIONS]

.. option:: -gl <glue_connection>, --glue_connection <glue_connection>

   AWS Glue connection name to connect via awswrangler

.. option:: -ar <aws_region>, --aws_region <aws_region>

    Default aws to fetch data from

.. option:: --version

   Display the version and exit.

.. option:: --help

   Display a short usage message and exit.
