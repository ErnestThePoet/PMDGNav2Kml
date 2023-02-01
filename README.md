# PMDGNav2Kml
This script makes it possible to convert waypoints and navaids from PMDG-format navdata into a kml file for Google Earth.

In "SETTINGS SECTION" of `main.py`, set your desired lat&lon range and run the script. Then open the output kml file with Google Earth, and you will see all the waypoints and navaids in the range you set. (Note that too many placemarks will make Google Earth significantly slow!)

To use a newer version of navdata, replace the `wpNavAID.txt` and `wpNavFIX.txt` files with corresponding ones in your PMDG navdata folder.

<image src="https://github.com/ErnestThePoet/PMDGNav2Kml/blob/master/screenshot.png"/>