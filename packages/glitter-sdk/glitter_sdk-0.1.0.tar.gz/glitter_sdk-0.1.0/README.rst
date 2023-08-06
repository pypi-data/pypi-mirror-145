
:Info: See `the glitter site`_  for more information. See `glitter-sdk-py`_ for the latest source.
:Documentation: Available at `glitter-sdk-py.readthedocs.io`_
:Author: ted

.. contents:: Table of Contents

=========================
 Installation
=========================

glitter sdk is in the `Python Package Index`_.
This tutorial walks you through how to set up glitter-sdk-py_ for local development.

The glitter Python Driver depends on:

1. Python 3.5+
2. A recent Python 3 version of pip
3. A recent Python 3 version of setuptools

Installing with pip
---------------------

We recommend using pip_ to install glitter_sdk on all platforms:

.. code-block:: bash

    $ python3 -m pip install glitter_sdk

To get a specific version of glitter:

.. code-block:: bash

    $ python3 -m pip install glitter_sdk==0.1.0

To upgrade using pip:

.. code-block:: bash

    $ python3 -m pip install --upgrade glitter_sdk

Dependencies
---------------------

You can install all dependencies automatically with the following command:

.. code-block:: bash

    $ python3 -m pip install glitter_sdk[requests]


Installing from source
----------------------------------

If you’d rather install directly from the source (i.e. to stay on the bleeding edge), install the C extension dependencies then check out the latest source from GitHub and install the driver from the resulting tree:

.. code-block:: bash

    $ git clone https://github.com/glitternetwork/glitter-sdk-py glitter-sdk-py
    $ cd glitter-sdk-py/
    $ python3 setup.py install


.. _the glitter site: https://glitterprotocol.io
.. _glitter-sdk-py: https://github.com/glitternetwork/glitter-sdk-py
.. _glitter-sdk-py.readthedocs.io: https://glitter-sdk-py.readthedocs.io/en/latest/index.html
.. _pip: https://pypi.org/project/pip/
.. _Python Package Index: https://pypi.org/project/glitter_sdk/
