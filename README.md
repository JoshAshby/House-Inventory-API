Project Blue Ring:
=============
* Joshua P Ashby
* 2011
* joshuaashby@joshashby.com
* http://joshashby.com
* http://www.flickr.com/photos/joshashby/
* https://github.com/JoshAshby

Foreword:
--------------
Please note that this is a major work in progress, the API maybe broken at anytime, and the URL scheme may change without warning, should a better solution present itself.
Also throughout the documentation, the word peak comes up. Peak referes to the stated interval on which a restock has just happened, till the next restock or the current day.

License:
-------------
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.

Abstract:
-------------
A RESTful API written in Python with the web.py Python web framwork which handles all the nasty stuff for keeping a basic inventory

API Info:
--------------
Coming soon after this Python branch of the API is finished.

	/ General home page currently, It will eventually be the web front address... I think

The following return JSON formated data (all POST/PUT/DELETE calls are OAuth protected)

	/product/
		GET - Returns the total list of products
		POST - Places a new product into the database.
	/product/<barcode>/
		GET - Returns the info for the specified product
		PUT - Updated the current product
		DELETE - Deletes the current product
	/category/ 
		GET - Lists the total categories.
	/category/<category _name>/
		GET - Lists the products inside of the category.
	/category/<category _name>/tag/<tag_name>/
		GET - Lists the products which have the matching tags inside of the listed category.
	/tag/
		GET - Lists the total tags in the database.
	/tag/<tag_name>/
		GET - Lists all the products in the given tag.
	/log/<barcode>/
		GET - Lists the usage log for the given product.

All pictures can be accessed at either ``/pictures/barcode.fileextension`` or ``/thumb/barcode_thumb.fileextension``

Database Info:
--------------------------
Everything is stored in JSON format inside of a couchDB.
This means users, products and views are all one and the same to the database. Views for seperating each type are included in ``couchdb/``

Other info:
-----------------

Nothing yet!

Libraries used:
----------------------

Python:

* oauth2
* datetime
* re
* json
* web.py
* mod_wsgi
* linear.py (aka: ashmath.py)
* ashpic.py
* auth.py
* account.py
* PIL (Python Image Library)
* hashlib
* couchdbkit

Examples and testing scripts also use:

* poster
* urllib2