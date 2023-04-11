#!/usr/bin/env python3

#Simple inventory - take an xls file and sort for warranty/expiry purposes
#RST output files for each category, these can then be used in a wiki or similar

#Author David Simpson, 2022, 2023

#Example XLS file format
#Software name Quantity/Entitlements License Number Expiry Vendor Purchased from User Management Status Comment


import glob
from pathlib import Path
import os
import sys
from tabulate import tabulate
import pandas as pd

############START GLOBALS ################

DayThresh=90
DayThresh_str=str(DayThresh)
#DayThresh1=90 #2nd var if ever needed, would need work to incorporate

#This form is Needed in source xls
DateFormat="'%d-%m-%y'"
#see tabulate
OutputTableType="'rst'"

MainColumn='WarrantyEnd' #Call this whatever you want, Expiry/WarrantyEnd, but it must be present in the XLS and be the source of dates
SecondaryColumn='Hostname' #This could be Hostname, Software name or anything - a relevant second column to sort by - must be present

#titles here are mapped to output file
TitleTuple=('NO WARRANTY/LICENSE MAY REQUIRE IMMEDIATE ATTENTION!',
             'ITEMS WITH LESS THAN: '+DayThresh_str+' Days - REQUIRE IMMEDIATE ATTENTION!',
             'ITEMS WITH: '+DayThresh_str+' Days or more remaining')
             
############END GLOBALS ##################

#find cwd
WORKDIR=os.getcwd()

#glob to find files
LATESTXLSPATH=Path(WORKDIR+'/inventory_py_*.xls')
print(LATESTXLSPATH)

#*** BEWARE WE USE MTIME HERE TO DETERMINE LATEST FILE!!!***

#get file to process (newest)
LATESTXLS=max(glob.iglob(LATESTXLSPATH.name), key=os.path.getmtime)

#read in, note that D-M-Y needed in input
df=pd.read_excel(LATESTXLS, index_col=None, parse_dates=[MainColumn], date_format=eval(DateFormat))

#deal with errors, errors become NaT, not a time
df[MainColumn]=pd.to_datetime((df.eval(MainColumn)), dayfirst=True, errors='coerce')

#USE TO FILTER NULL - null (or NaT) being no warranty data in field
df_filtered_in_null=(df[df[MainColumn].isnull()])

#get the date ahead
DateNDaysAhead = pd.Timestamp('now').floor('D') + pd.Timedelta(+DayThresh, unit='D')

#create slices
slice1 = df[df.eval(MainColumn) < DateNDaysAhead].sort_values(by=[MainColumn,SecondaryColumn])
slice2 = df[df.eval(MainColumn) >= DateNDaysAhead].sort_values(by=[MainColumn,SecondaryColumn])

#tabulate the two dfs of interest
table_var0=tabulate(df_filtered_in_null, headers='keys', tablefmt=eval(OutputTableType)) #no date/expired entries
table_var1=tabulate(slice1, headers='keys', tablefmt=eval(OutputTableType)) #fall within threshold
table_var2=tabulate(slice2, headers='keys', tablefmt=eval(OutputTableType)) #all others outside the threshold but not no date/expired entries

#write files
for iter in range(3):
  iter_str=(str(iter))
  this_file="init"
  with open(WORKDIR+"/title"+iter_str+".inc", 'w', encoding="utf-8") as this_file:
    this_file.write(TitleTuple[iter])
    this_file.close()
    this_file="done"
  this_file="init"
  
  with open(WORKDIR+"/content"+iter_str, 'w', encoding="utf-8") as this_file:
    if iter == 0:
      this_file.write(table_var0)
      this_file.close()
    if iter == 1:
      this_file.write(table_var1)
      this_file.close()
    if iter == 2:
      this_file.write(table_var2) 
      this_file.close()
  this_file="done"

#exit 0
sys.exit(0)
