# simple_inventory

Simple inventory - a rudimentary python3 script to turn an XLS into a RST files, based on some expiry criteria (number of days ahead).

The output could be made to be something else not RST.

It's rough and ready and could be improved.

Example XLS file content is included here in this README.

# Why

Needed something to process an inventory spreadheet (that anyone could maintain/upload) and regularly check for expiry of items. Thus, a page can be viewed that will always be reflective of status (once the output is re-assembled somewhere).

# How to use it? i)

Look at the script - ```MainColumn``` and ```SecondaryColumn``` values in particular, these are the two columns that will be sorted by. 

Create your XLS file (inventory).

The XLS file should take the name ```inventory_py_DDMMYY.xls``` (e.g. <i>inventory_py_210422.xls</i>). Beware that currently the script uses ```mtime``` to determine that this latest named file is the latest - its assumed your latest file would have the newest date in its name.

- Simply drop in an XLS file into the same directory (```cwd```) as this script.
- Reference and adapt the script accordingly to suit the XLS headings. 
- Check the ```DayThresh``` value is suitable - this governs how far to look ahead to consider approaching expiry.
- Run the script.
- Output is in ```cwd```
- RST files are found as output. These are headings files and associated content files.
- Do what you will with these - e.g. combine them and serve on a wiki/webbserver.

# How to use it? ii)

- Set it up in gitlab CI/CD and push to your wiki.


# Example XLS content

Create an XLS file like this: **inventory_py_210422.xls** with:

| Hostname |	ServiceTag	| Manufacturer| Model | WarrantyEnd | SupportEntity | Type | Subtype | User |	Management | Status | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| somehost1	| 123456 | Dell | Dell123	| 01-06-26 | Dell |	Storage	Server | Lab1 |	ENG1 | Active | Production |
| somehost2 | 910784 | HP | HP123	| 01-01-22 | HP	| Storage	Server | Lab2 | ENG2 | InActive |Retiring |

# Results of processing example XLS content

6 files produced. Hardcoded titles from script.
- content0.inc
- content1.inc
- content2.inc
- title0.inc
- title1.inc
- title2.inc

## What the resultant files look like

**title0.inc** file:

```NO WARRANTY/LICENSE MAY REQUIRE IMMEDIATE ATTENTION!```

**content0.inc** file:
```
==========  ============  ==============  =======  =============  ===============  ======  =========  ======  ============  ========  =========
Hostname    ServiceTag    Manufacturer    Model    WarrantyEnd    SupportEntity    Type    Subtype    User    Management    Status    Comment
==========  ============  ==============  =======  =============  ===============  ======  =========  ======  ============  ========  =========
==========  ============  ==============  =======  =============  ===============  ======  =========  ======  ============  ========  =========
```

COMMENT ON ABOVE: table produced, but no entries in this table (as the XLS did have <i>WarrantyEnd</i> dates in both cells/items)

--------------

**title1.inc** file: 

```ITEMS WITH LESS THAN: 90 Days - REQUIRE IMMEDIATE ATTENTION!```

**content1.inc** file:
```
====  ==========  ============  ==============  =======  ===================  ===============  ==============  =========  ======  ============  ========  =========
  ..  Hostname      ServiceTag  Manufacturer    Model    WarrantyEnd          SupportEntity    Type            Subtype    User    Management    Status      Comment
====  ==========  ============  ==============  =======  ===================  ===============  ==============  =========  ======  ============  ========  =========
   1  somehost2         910784  HP              HP123    2022-01-01 00:00:00  HP               Storage Server  Lab2       ENG2    InActive      Retiring        nan
====  ==========  ============  ==============  =======  ===================  ===============  ==============  =========  ======  ============  ========  =========
```

COMMENT ON ABOVE: table produced, an entry - as the XLS was found to have an expired item.

--------------

**title2.inc** file:

``` ITEMS WITH: 90 Days or more remaining```

**content2.inc** file:
```
====  ==========  ============  ==============  =======  ===================  ===============  ==============  =========  ======  ============  ==========  =========
  ..  Hostname      ServiceTag  Manufacturer    Model    WarrantyEnd          SupportEntity    Type            Subtype    User    Management    Status        Comment
====  ==========  ============  ==============  =======  ===================  ===============  ==============  =========  ======  ============  ==========  =========
   0  somehost1         123456  Dell            Dell123  2026-06-01 00:00:00  Dell             Storage Server  Lab1       ENG1    Active        Production        nan
====  ==========  ============  ==============  =======  ===================  ===============  ==============  =========  ======  ============  ==========  =========
```
COMMENT ON ABOVE: table produced, an entry - as the XLS was found to have an item with plenty of remaining warranty.

