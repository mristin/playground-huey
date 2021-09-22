***************
playground-huey
***************

.. image:: https://github.com/mristin/playground-huey/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/mristin/playground-huey/actions/workflows/ci.yml
    :alt: Continuous Integration

Play with Huey queues to see how they work in Windows.

Setup
======
Create the virtual environment in the repository root:

.. code-block::

    python3 -m venv venv

Activate it on Windows:

.. code-block::

    venv\Scripts\activate

or on Linux / Mac OSX:

.. code-block::

    source venv/bin/activate

Install the dependencies and the playground in the editable mode (so that it appears on your ``PYTHONPATH``):

.. code-block::

    pip3 install -e .


Start
=====
Make sure you activated the virtual environment (see Section "Setup" above).

You have to start the Huey consumers first:


.. code-block::

    huey_consumer playground.jobs.HUEY --workers 4

Then start the backend:

.. code-block::

    python playground\backend.py

Finally, execute the test client which will send a request an endpoint:

.. code-block::

    python playground\test_client.py

Development
===========
Make sure you activated the virtual environment (see Section "Setup" above).

Install development dependencies:

.. code-block::

    pip3 install -e .[dev]

Run the pre-commit checks:

.. code-block::

    python precommit.py

If you want to automatically overwrite the files (*e.g.*, to reformat):

.. code-block::

    python precommit.py --overwrite
