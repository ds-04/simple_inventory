#!/usr/bin/env python3

#Simple inventory - take an xls file and sort for warranty/expiry purposes
#RST output files for each category, these can then be used in a wiki or similar

#Author David Simpson, 2022

#Example XLS file format
#Software name	Quantity/Entitlements	License Number	Expiry	Vendor	Purchased from	User	Management	Status	Comment

import csv
import datetime
from tabulate import tabulate
import glob
import pandas as pd
import numpy as np
from pathlib import Path
import os

DayThresh=90
DayThresh_str=str(DayThresh)
#DayThresh1=90 #2nd var if ever needed, would need work to incorporate

MainColumn='WarrantyEnd' #Call this whatever you want, Expiry/WarrantyEnd, but it must be present in the XLS
SecondaryColumn='Hostname' #This could be Hostname, Software name or anything - a relevant second column to sort by - must be present
dataframeMainColumn='df.WarrantyEnd' #REDUNDANT in this code, TODO ideally this would be used below, where df.WarrantyEnd is appearing

#find cwd
WORKDIR=os.getcwd()

#glob to find files
latest_xls_path=Path(WORKDIR+'/inventory_py_*.xls')
print(latest_xls_path)

#BEWARE WE USE MTIME HERE TO DETERMINE LATEST FILE!!!

#get file to process (newest)
latest_xls_filename=max(glob.iglob(latest_xls_path.name), key=os.path.getmtime)

#read in
df=pd.read_excel(latest_xls_filename, index_col=None)

#deal with errors
df.WarrantyEnd = pd.to_datetime(df.WarrantyEnd, dayfirst=True, errors='coerce') #errors become NaT <<< can  dataframeMainColumn var be used?

#USE TO FILTER NULL - null being no warranty data in field
df_filtered_in_null=(df[df[MainColumn].isnull()])

#get the date ahead
date_N_days_ahead = (pd.Timestamp('now').floor('D') + pd.Timedelta(+DayThresh, unit='D')).strftime('%y-%m-%d')

#use to deubg
#print(date_N_days_ahead)
#print("These items should be checked immediately")
#print(df.Expiry)
slice1 = df[df.WarrantyEnd.dt.strftime('%y-%m-%d') < date_N_days_ahead].sort_values(by=[MainColumn,SecondaryColumn])

#use to debug
#print("ALL OTHER ENTRIES") # won't have expired/no date entries
slice2 = df[df.WarrantyEnd.dt.strftime('%y-%m-%d') >= date_N_days_ahead].sort_values(by=[MainColumn,SecondaryColumn])

#tabulate the two dfs of interest
table_var_null=tabulate(df_filtered_in_null, headers='keys', tablefmt='rst') #no date/expired entries
table_var0=tabulate(slice1, headers='keys', tablefmt='rst') #fall within threshold
table_var1=tabulate(slice2, headers='keys', tablefmt='rst') #all others outside the threshold but not no date/expired entries

#Write title0 then data/table0 - no warranty or expired
f1 = open(WORKDIR+"/title0.inc", "w")
f1.write("NO WARRANTY/LICENSE MAY REQUIRE IMMEDIATE ATTENTION!") #This is the first title, for title file0
f1.close()
f2 = open(WORKDIR+"/content0.inc", "w")
f2.write(table_var_null)
f2.close()

#Write title1 then data/table1 - expiring/threshold
f3 = open(WORKDIR+"/title1.inc", "w")
f3.write("ITEMS WITH LESS THAN: "+DayThresh_str+" Days - REQUIRE IMMEDIATE ATTENTION!") #This is the second tile, title file1
f3.close()
f4 = open(WORKDIR+"/content1.inc", "w")
f4.write(table_var0)
f4.close()

#Write title2 then data/table2 - all other hosts
f5 = open(WORKDIR+"/title2.inc", "w")
f5.write("ITEMS WITH: "+DayThresh_str+" Days or more remaining") #This is the third tile, title file2
f5.close()
f6 = open(WORKDIR+"/content2.inc", "w")
f6.write(table_var1)
f6.close()
