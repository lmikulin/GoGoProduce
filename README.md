GoGoProduce
===========
This is a console Python based grocery store checkout system.

The "produce" and "promotions" information is pulled from the inventory.xml file. This was written as a data file to have it separated from the program and in anticipation that it will change frequently.

Similarly the promo_functions.py file was written as a separate module for extensibility since different types of promotions may come up.

System Requirements
-------------------
This program was written and tested on Python 2.7.6 and is supported for the 2.7.x releases.

It was tested on a mac (OS X Yosemite Beta 10.10) and windows 7 platforms.

Usage
-----
The program can be run in interactive mode:
$ python produce.py

or with a test file - I've provided a sample test file:
$ python produce.py < sample_test.txt 

Expected Input
--------------
The program accepts any of the known fruits** as input as well as 'help'.

Return indicates the list is done and the receipt is printed. Similarly when data is streamed from the data file EOF (or return) indicates the end of the grocery list and the receipt is printed.

Any unknown produce is ignored.

**known fruits means all the fruits found in the inventory.xml file

Misc Notes
----------
This program imports the xml.etree.ElementTree module

Contact
-------
Hope you enjoy buying fruit at GoGoProduce! :)
I can be reached at: lmikulin@gmail.com
