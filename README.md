traffic-analysis
================

A framework to analyze traffic incident reports from the Bing Maps API and predict future incident levels

Installing the Dependencies
-----------
# Install [Pip](http://www.pip-installer.org/en/latest/installing.html)
# In this folder run `pip install -r requirements.txt`

Exporting an ARFF file
----------------------
Simply run `python export_arff.py [in_file.json] [out_file.arff] [conf_file.json]`

The Configuration File
---------------------
An example configuration file can be found at `conf/example.json`.  The maps and filters listed will be run in the order listed in your conf file.  Attributes have three fields: the name of the attribute in the exported ARFF file, the [JSON path](http://goessner.net/articles/JsonPath/) to the attribute in each instance, and the type of attribute (NOMINAL, NUMERIC, and INTEGER are currently supported).