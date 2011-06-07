Project Blue Ring:
=============
* Joshua P Ashby
* 2011
* joshuaashby@joshashby.com
* http://joshashby.com
* http://www.flickr.com/photos/joshashby/
* https://github.com/JoshAshby

Forword:
--------------
Please note that this is a major work in progress, the API maybe broken at anytime, and the URL scheme may change without warning, should a btter solution present itself.
Also throughout the documentation, the word peak comes up. Peak referes to the stated interval on which a restock has just happened, till the next restock or the current day.

Please note: The clients do not work on this branch. They are setup for the Perl API version's URL scheme and as a result are not compatable with this branch. They will be updated, after more work has been completed on the API.

License:
-------------
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.

Abstract:
-------------
A simple API written in Python which handles all the nasty stuff for keeping a basic inventory

This branch of the API uses web.py, MySQL and mod_wsgi instead of Perl for the API, however the client and the webinterface 
will remain the same across all branches (however the code base will have to change due to url scheme changes). If this ends up working better, it may be adopted as the master branch, and the Perl-OO 
branch (the main API branch currently) will be left behind. (Which has already happened.)

This branch may also intergrate R as the main statistics generation for the products. (It does but it doesn't, because rpy2 doesn't like to run in a web.py session, and makes the program hang without any errors...) as a result, This branch includes a copy of linear.py, my own Vector math type for Python which is used for the linear math done in the stats function.

API Info:
--------------
Coming soon after this Python branch of the API is finished.

	/ General home page currently, It will eventually be the web front address... I think

The following return JSON formated data:

	/product/dog987/info/ Info for the product whos barcode  comes after the /product/
	/product/dog987/delete/ Delete said product with barcode stated
	/product/dog987/Beagle/3/A+dog+with+brown+and+black+and+white+fur./add/ Add the given product, the url should be: barcode, name, quantity, description
	/product/dog987/Beagle/3/A+dog+with+brown+and+black+and+white+fur./update/ Update the given product, the url should be: barcode, name, quantity, description
	/product/ get the total products
	/product/names/ only the names and barcodes of all the products for auto complete
	/product/dog987/log/ display the quantity change log for the product
	/product/dog987/stats/ coming soon

Database Info:
--------------------------

Products are stored in a MySQL database with the following columns:
``[id][name][description][barcode][quantity][average][coef][flag]``

	[id] is just an arbitrary id number which may go away in future versions of the database as none of the code uses it.
	[name] is the name of the product
	[description] is the product description
	[barcode] is the barcode
	[quantity] is the current quantity
	[average] last 5 ratios of the number of products over days per each peak
	[coef] Storage of the coefficents for the products last ran regression line
	[flag] is also reserved but can be manually set as it's just H,M or L for high priority, medium priority, and low priority, in terms of the quantity left. This will be used for shopping list generation later on when thats added to the API.

Product use is stored in a second MySQL table which is formated like so:
``[barcode][quantity][date][reason]``

	[barcode] is the product barcode
	[quantity] is the products new quantity at the time the entry was added (after a change has happened to the quantity)
	[date] name says it all
	[reason] either restock or soon to be the order ID this will be tied in with a third table for storing orders

Other info:
-----------------

The API takes care of updating a product, searching and returning information about a product, returning the whole database for a total inventory, returning the usage log of the product, and stats on the product (only the linear regression of the data is available right now).
All returned data is in JSON format, and all queries should be by the barcode even though some types can take either name or barcode.

It is assumed you know how to install the Python libraries needed, place the Python scripts on a web server with 
Python and mod_wsgi and web.py and MySQL installed, along with run Python scripts and work SL4A.

Libraries used:
----------------------

Python:
* datetime
* re
* json
* web.py
* mod_wsgi
