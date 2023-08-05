***************
Prerequisites
***************

- Python3 version 3.7 or greater
- pip

********
Install
********

pip
====
Preferred method

Install
--------

.. tabbed:: pip call

   .. code-block:: sh
      :caption: pip

      pip install psprint


.. tabbed:: python module call

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip install psprint


Update
-------

.. tabbed:: pip call

   .. code-block:: sh
      :caption: pip

      pip install -U psprint


.. tabbed:: python module call

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip install -U psprint


Uninstall
----------

.. tabbed:: pip call

   .. code-block:: sh
      :caption: pip

      pip uninstall -y psprint

.. tabbed:: python module call

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip uninstall -y psprint



`pspman <https://github.com/pradyparanjpe/pspman>`__
=====================================================

(Linux only)

For automated management: updates, etc


Install
--------

.. code-block:: sh

   pspman -s -i https://gitlab.com/pradyparanjpe/psprint.git



Update
-------

.. code-block:: sh

    pspman


*That's it.*


Uninstall
----------

Remove installation:

.. code-block:: sh

    pspman -s -d psprint

