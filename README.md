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
A simple API written in Perl which handles all the nasty stuff for keeping a basic inventory. It also comes with a two front ends, a client side which is a Python GUI written in PyQt4, and a web front end which is generated by Perl, however jQuery/javascript is used for interaction with the API.

API Info:
--------------

The available querys to the API currently are (All return data and all data is in JSON format):
	gui will open the web front end if set to ``y``
	type_of_query sets what type of query your going to be calling.
Types include:
	product_info returns a single products info based off of barcode
	total_inventory returns the whole product database
	add_product adds a product
	update_product updates a product
	remove_product removes a product based off of barcode
	return_log returns the usage log based off of barcode
	gen_stat returns the slope, intercept and data points for the stats plots based off of barcode
	names returns all the names and barcodes in the database (mainly for auto complete)
	return_log_flot same as return_log however data is formated for flot to read (not currently used as it requires the dates to be converted based off of barcode
	return_stat_flot returns the points of the stats graph in a format flot can read based off of barcode
	gen_stat_flot returns the slope and intercept for flot to use based off of barcode

###API Examples:

	api.pl?gui=y
	api.pl?type_of_query=product_info&query=718103025027
	api.pl?type_of_query=total_inventory
	api.pl?type_of_query=add_product&name=Product+name&query=718103025027&description=Description+of+product&quantity=3&flag=L
	api.pl?type_of_query=update_product&name=Product+name&query=718103025027&description=Description+of+product&quantity=3&flag=L
	api.pl?type_of_query=remove_product&query=718103025027
	api.pl?type_of_query=return_log&query=718103025027
	api.pl?type_of_query=gen_stat&query=718103025027 
	api.pl?type_of_query=names
	api.pl?type_of_query=return_log_flot&query=718103025027
	api.pl?type_of_query=return_stat_flot&query=718103025027
	api.pl?type_of_query=gen_stat_flot&query=718103025027


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

It is assumed you know how to install the Perl and Python libraries needed, place the Perl scripts on a web server with Perl and mod_perl installed, along with run Python scripts and work SL4A.

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

Perl (available from CPAN):

* CGI
* DBI
* DBD::mysql
* JSON
* Statistics::LineFit
* DateTime/DateTime::Format::MySQL

Javascript/html/css:

* jQuery and jQuery UI http://jquery.com/
* flexigrid for jQuery http://flexigrid.info/
* editableText for jQuery https://github.com/valums/editableText
* flot for jQuery http://code.google.com/p/flot/
* The wonderful Aristo theme for jQuery UI https://github.com/taitems/Aristo-jQuery-UI-Theme
* bluetrip CSS grid and type setting framework http://bluetrip.org/
* Less.js http://lesscss.org/