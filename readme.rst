Api Client Documentation
========================

.. contents::

Installation
------------

Clone the repo in your laptop:

.. code-block::

  # https://github.com/jkleinerman/nirvana-challenge.git


Usage
-----

If you want to get data for ``member_id = 45`` and Coalesce Strategy: ``mean``, run:

.. code-block::

  # python client.py -i 45 -s mean

If you run the program with ``-h`` option, the following help will be printed:

.. code-block::

  usage: client.py [-h] -i MEMBER_ID -s {mean,max,min}

  Connect and coalesce data

  optional arguments:
    -h, --help            show this help message and exit
    -i MEMBER_ID, --member-id MEMBER_ID
                          Member ID
    -s {mean,max,min}, --strategy {mean,max,min}
                          Coalesce Strategy


Output
------

The output in standard out will be something like this:

.. code-block::

  For the following APIs:
  - https://api1.com
  - https://api2.com
  - https://api3.com
  Using member ID: 45 and Coalesce Strategy: mean
  The result is: {"deductible": 1134, "stop_loss": 11530, "oop_max": 5442.67}


Testing
-------

If you want to test the results, run ``testing.py``.

.. code-block::

  # python testing.py

It will test different different Coalesce Strategies showing an output like this:

.. code-block::

  Testing with member_id: 1 and strategy: min
  Test: PASS
  Testing with member_id: 4 and strategy: max
  Test: PASS
  Testing with member_id: 79 and strategy: mean
  Test: PASS




Comments
--------

For this code challenge, I coded a ``server.py`` module.
It simulates the API server.
Every time the client connects the server, it responds with different values of:
``deductible``,``stop_loss`` and ``oop_max`` gotten randomly from  intervals received as argument.
It uses the member ID and API number from the URL to generate the random values.
