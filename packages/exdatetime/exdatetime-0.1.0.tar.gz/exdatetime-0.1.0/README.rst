Exdatetime is designed to extend from the module datetime of Python.

Installation
------------

.. code:: sh

   pip install exdatetime

Usage
-----

Import the whole module at the beginning of your progam:

.. code:: python

   from exdatetime import *

Functions
---------

-  ``isleap(y, isjulian = True)``: Returns whether a year is leap or
   not.
-  ``daysofmonth(y, m, isjulian = True)``: Returns the days of a
   specific month.
-  ``cmpdate(d1, d2)``: Compares dates ``d1`` and ``d2``, returns 0 if
   equals, 1 if d1 is later, or -1 if d1 is earlier.
-  class ``julian``:

   -  ``init()``: Initialize the class. This could be automatically
      executed while running other functions from this class.
   -  ``getdate(x)``: Returns the date transferred from the given julian
      cardinal date number (x) in the form of the class “date”.
   -  ``todate(x)``: Similar to above, but returns in the form of a
      string.
   -  ``tojulian(y, m, d)``: Transfers a specific date to a julian
      cardinal date number.

Examples
--------

.. code:: python

   from exdatetime import *
   print(isleap(2022)) # False
   print(daysofmonth(2000, 2)) # 29
   print(cmpdate(date(2022, 4, 1), date(2022, 4, 5))) # -1
   print(julian.todate(2459161)) # 2020 11 7
   print(julian.tojulian(2022, 4, 5)) # 2459675