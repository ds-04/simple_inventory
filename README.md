# simple_inventory

Simple inventory - a rudimentary python3 script to turn an XLS into a RST files, based on some expiry criteria (number of days ahead).

The output could be made to be something else not RST.

It's rough and ready and could be improved.

An example XLS is included here.

# Why

Needed something to process an inventory spreadheet (that anyone could maintain/upload) and regularly check for expiry of items. Thus, a page can be viewed that will always be reflective of status.

# How to use it? i)

Look at the script - ```MainColumn``` and ```SecondaryColumn``` values in particular. Create your XLS file (inventory).

The XLS file should take the name ```inventory_py_DDMMYY.xls``` (e.g. inventory_py_210422.xls)

- Simply drop in an XLS file into the same directory (```cwd```) as this script
- Reference and adapt the script accordingly to suit the XLS headings
- Run the script
- Output is in ```cwd```
- RST files and heading files are found
- Do what you will with these - e.g. serve on a wiki

# How to use it? ii)

- Set it up in gitlab CI/CD and push to your wiki
