UNICEF Auth Helper
==================


Installation
------------

.. code-block:: bash

    pip install unicef-utils


Setup
-----

Add ``unicef_business_areas`` to ``INSTALLED_APPS`` in settings

.. code-block:: bash

    INSTALLED_APPS = [
        'django_admin_extra_buttons',
        'unicef_business_areas',
    ]


Usage
-----

TODO

Contributing
------------

Environment Setup
~~~~~~~~~~~~~~~~~

To configure the development environment

.. code-block:: bash

    $ make develop


Coding Standards
~~~~~~~~~~~~~~~~

See `PEP 8 Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ for complete details on the coding standards.

To run checks on the code to ensure code is in compliance

.. code-block:: bash

    $ make lint


Testing
~~~~~~~

Testing is important and tests are located in `tests/` directory and can be run with;

.. code-block:: bash

    $ make test

Coverage report is viewable in `build/coverage` directory, and can be generated with;



Links
~~~~~

+--------------------+----------------+--------------+--------------------+
| Stable             | |master-build| | |master-cov| |                    |
+--------------------+----------------+--------------+--------------------+
| Development        | |dev-build|    | |dev-cov|    |                    |
+--------------------+----------------+--------------+--------------------+
| Source Code        |https://github.com/unicef/unicef-utils               |
+--------------------+----------------+-----------------------------------+
| Issue tracker      |https://github.com/unicef/unicef-utils/issues        |
+--------------------+----------------+-----------------------------------+


.. |master-build| image:: https://secure.travis-ci.org/unicef/unicef-utils.svg?branch=master
                    :target: http://travis-ci.org/unicef/unicef-utils/

.. |master-cov| image:: https://codecov.io/gh/unicef/unicef-utils/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/unicef/unicef-utils

.. |dev-build| image:: https://secure.travis-ci.org/unicef/unicef-utils.svg?branch=develop
                  :target: http://travis-ci.org/unicef/unicef-utils/

.. |dev-cov| image:: https://codecov.io/gh/unicef/unicef-utils/branch/develop/graph/badge.svg
                    :target: https://codecov.io/gh/unicef/unicef-utils



Compatibility Matrix
--------------------

Stable
~~~~~~

.. image:: https://travis-matrix-badges.herokuapp.com/repos/unicef/unicef-utils/branches/master


Develop
~~~~~~~

.. image:: https://travis-matrix-badges.herokuapp.com/repos/unicef/unicef-utils/branches/develop
