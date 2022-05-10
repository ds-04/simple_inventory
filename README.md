# simple_inventory

Simple inventory - a rudimentary python3 script to turn an XLS into a RST files, based on some expiry criteria (number of days ahead).

The output could be made to be something else not RST.

It's rough and ready and could be improved.

Example XLS file content is included here in this README.

# Why

Needed something to process an inventory spreadheet (that anyone could maintain/upload) and regularly check for expiry of items. Thus, a page can be viewed that will always be reflective of status (once the output is re-assembled somewhere).

# How to use it? i)

Look at the script - ```MainColumn``` and ```SecondaryColumn``` values in particular. Create your XLS file (inventory).

The XLS file should take the name ```inventory_py_DDMMYY.xls``` (e.g. <i>inventory_py_210422.xls</i>). Beware that currently the script uses ```mtime``` to determine that this latest named file is the latest - its assumed your latest file would have the newest date in its name.

- Simply drop in an XLS file into the same directory (```cwd```) as this script
- Reference and adapt the script accordingly to suit the XLS headings
- Run the script
- Output is in ```cwd```
- RST files and heading files are found
- Do what you will with these - e.g. serve on a wiki

# How to use it? ii)

- Set it up in gitlab CI/CD and push to your wiki


# Example XLS content

Create a XLS file like this: **inventory_py_210422.xls** with:

| Hostname |	ServiceTag	| Manufacturer| Model | WarrantyEnd | SupportEntity | Type | Subtype | User |	Management | Status | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| somehost1	| 123456 | Dell | Dell123	| 01-06-26 | Dell |	Storage	Server | Lab1 |	ENG1 | Active | Production |
| somehost2 | 910784 | HP | HP123	| 01-01-22 | HP	| Storage	Server | Lab2 | ENG2 | InActive |Retiring |


