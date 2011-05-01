House Inventory API:
=============
* Joshua P Ashby
* 2011
* joshuaashby@joshashby.com
* http://joshashby.com
* http://www.flickr.com/photos/joshashby/
* https://github.com/JoshAshby

License:
-------------
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.

Abstract:
-------------
A simple API written in Python which handles all the nasty stuff for keeping a basic inventory. It also comes with a 
two front ends, a client side which is a Python GUI written in PyQt4, and a web front end which is generated by Python, 
however jQuery/javascript is used for interaction with the API.

This branch of the API uses web.py, MySQL and mod_wsgi instead of Perl for the API, however the client and the webinterface 
will remain the same across all branches. If this ends up working better, it may be adopted as the master branch, and the Perl-OO 
branch (the main API branch currently) will be left behind.

This branch may also intergrate R as the main statistics generation for the products.

API Info:
--------------
Coming soon after this Python branch of the API is finished.

Database Info:
--------------------------

Products are stored in a MySQL database with the following columns:
``[id][name][description][barcode][quantity][average][flag]``

	[id] is just an arbitrary id number which may go away in future versions of the database as none of the code uses it.
	[name] is the name of the product
	[description] is the product description
	[barcode] is the barcode
	[quantity] is the current quantity
	[average] is reserved for when more stats functions are added in to the API
	[flag] is also reserved but can be manually set as it's just H,M or L for high priority, medium priority, and low priority, in terms of the quantity left. This will be used for shopping list generation later on when thats added to the API.

Product use is stored in a second MySQL table which is formated like so:
``[barcode][quantity][date][date_time]``

	[barcode] is the product barcode
	[quantity] is the products new quantity at the time the entry was added (after a change has happened to the quantity)
	[date] is not used currently
	[date_time] is a MySQL timestamp which is automatically set by the database for generating stats and plotting the use over time.

Other info:
-----------------

The API takes care of updating a product, searching and returning information about a product, returning the whole database for a total inventory, returning the usage log of the product, and stats on the product (only the linear regression of the data is available right now).
All returned data is in JSON format, and all queries should be by the barcode even though some types can take either name or barcode.

It is assumed you know how to install the Python libraries needed, place the Python scripts on a web server with 
Python and mod_wsgi and web.py and MySQL installed, along with run Python scripts and work SL4A.

Libraries used:
----------------------

Python:

* PyQt4
* numpy
* matplotlib
* httplib/urllib
* threading
* datetime
* bluetooth
* json
* web.py
* mod_wsgi

Javascript/html/css:

* jQuery and jQuery UI http://jquery.com/
* flexigrid for jQuery http://flexigrid.info/
* editableText for jQuery https://github.com/valums/editableText
* flot for jQuery http://code.google.com/p/flot/
* The wonderful Aristo theme for jQuery UI https://github.com/taitems/Aristo-jQuery-UI-Theme
* bluetrip CSS grid and type setting framework http://bluetrip.org/
* Less.js http://lesscss.org/
