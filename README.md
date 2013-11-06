traffic-analysis
================

A framework to analyze traffic incident reports from the Bing Maps API and predict future incident levels


To make an ARFF
-----
Run the following (using ruby 1.9 and python 2.7.5):
```bash
python ./pull_json.py
ruby ./export_arff.rb data/latest.json resources/paths latest.arff -r LatestData
```

That command looks at the paths file, pulls the requested paths into the ARFF,
and cleans the data so that WEKA can use it.

[Map URL](https://www.google.com/maps/ms?msid=216585993676216612684.0004e82e4266b9f739cda&msa=0&ll=37.580501,-122.01416&spn=0.636667,1.352692)
