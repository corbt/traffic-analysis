Traffic Analysis
================

A framework to analyze traffic incident reports from the Bing Maps API and predict future incident levels

Installing the Dependencies
-----------
1. Install [Pip](http://www.pip-installer.org/en/latest/installing.html)
2. In the top folder run `pip install -r requirements.txt`

Exporting an ARFF file
----------------------
Simply run `python export_arff.py [in_file.json] [out_file.arff] [conf_file.json]`

The Configuration File
---------------------
An example configuration file can be found at `conf/example.json`.  The maps and filters listed will be run in the order listed in your conf file.  
Attributes have three fields: 

1. The name of the attribute in the exported ARFF file, 
2. The [JSON path](http://goessner.net/articles/JsonPath/) to the attribute in each instance
3. The type of attribute (NOMINAL, NUMERIC, and INTEGER are currently supported).

Note that since attributes will be extracted *after* your maps are run, you can add computed attributes in a map and then reference them in the attribute list.  For example, in the `example.json` conf file the calculated attribute `hour` is referenced.
