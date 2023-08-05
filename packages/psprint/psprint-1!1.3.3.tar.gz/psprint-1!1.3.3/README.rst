#########
PSPRINT
#########

*********
Gist
*********

Source Code Repository
=======================

|source| `Repository <https://gitlab.com/pradyparanjpe/psprint.git>`__

|pages| `Documentation <https://pradyparanjpe.gitlab.io/psprint>`__

Badges
======

|Pipeline|  |Coverage|  |PyPi Version|  |PyPi Format|  |PyPi Pyversion|


************
Description
************

Prompt-String-like Print.

[ INFO ] Print statements with a flexible descriptor prefix for better
readability.

What does it do
===============

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8; mode: python; -*-

   print()
   print("*** WITHOUT PSPRINT ***")
   print("An output statement which informs the user")
   print("This statement requests the user to act")
   print("A debugging output useless to the user")
   print()

   from psprint import print
   print()
   print("*** WITH PSPRINT ***")
   print("An output statement which informs the user", mark=1)
   print("This statement requests the user to act", mark=2)
   print("A debugging output useless to the user", mark='bug')
   print ()


Screenshot:

.. figure:: docs/output.jpg
   :alt: screenshot

With extensive personalization `on-the-fly` and through configuration files


.. |Pipeline| image:: https://gitlab.com/pradyparanjpe/psprint/badges/master/pipeline.svg

.. |source| image:: https://about.gitlab.com/images/press/logo/svg/gitlab-icon-rgb.svg
   :width: 50
   :target: https://gitlab.com/pradyparanjpe/psprint.git

.. |pages| image:: https://about.gitlab.com/images/press/logo/svg/gitlab-logo-gray-stacked-rgb.svg
   :width: 50
   :target: https://pradyparanjpe.gitlab.io/psprint

.. |PyPi Version| image:: https://img.shields.io/pypi/v/psprint
   :target: https://pypi.org/project/psprint/
   :alt: PyPI - version

.. |PyPi Format| image:: https://img.shields.io/pypi/format/psprint
   :target: https://pypi.org/project/psprint/
   :alt: PyPI - format

.. |PyPi Pyversion| image:: https://img.shields.io/pypi/pyversions/psprint
   :target: https://pypi.org/project/psprint/
   :alt: PyPi - pyversion

.. |Coverage| image:: https://gitlab.com/pradyparanjpe/psprint/badges/master/coverage.svg?skip_ignored=true
