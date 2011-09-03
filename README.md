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
A RESTful API written in Python with web.py which handles all the nasty stuff for keeping a basic inventory

API Info:
--------------
Coming soon after this Python branch of the API is finished.

	/ General home page currently, It will eventually be the web front address... I think

The following return JSON formated data (all POST/PUT/DELETE calls are OAuth protected)

	/product/
		GET - Returns the total list of products
		POST - Places a new product into the database.
		PUT - 
		DELETE - 
	/product/<barcode>/
		GET - Returns the info for the specified product
		POST - 
		PUT - Updated the current product
		DELETE - Deletes the current product
	/category/ 
		GET - Lists the total categories
		POST - 
		PUT - 
		DELETE - 
	/category/<category _name>/
		GET - Lists the products inside of the category. 
		POST - 
		PUT - 
		DELETE - 
	/category/<category _name>/tag/<tag_name>/
		GET - Lists the products which have the matching tags inside of the listed category
		POST - 
		PUT - 
		DELETE - 
	/tag/
		GET - Lists the total tags in the database
		POST - 
		PUT - 
		DELETE - 
	/tag/<tag_name>/
		GET - Lists all the products in the given tag
		POST - 
		PUT - 
		DELETE - 
	/stat/<barcode>/
		GET - Lists the popularity, the rank and the predicted time till 0 units for the given product
		POST - 
		PUT - 
		DELETE - 
	/log/<barcode>/
		GET - Lists the usage log for the given product
		POST - 
		PUT - 
		DELETE - 

Note that the reponses for the admin calls may also return with ``{"COP": "dog"}`` which should mean a copy of that products barcode already exsist in the table. in this example, '``dog`` is the barcode of the product that there is a copy of.
Valid responses are ``[NED][NULL][NS][COP]`` ``[NED]`` meaning that there is Not Enough Data, ``[NULL]`` being mainly for the picture and thumbnail group indicating no picture or thumbnail is available, and ``[NS]`` being for Nothing Submitted, `[COP]`` meaning Copy Of Product meaning that a copy of that products barcode already exsists in the table.

All pictures can be accessed at either ``/pictures/barcode.fileextension`` or ``/thumb/barcode_thumb.fileextension``

Database Info:
--------------------------
This really needs to be updated!

Products are stored in a MySQL table: `products`
``[id][name][description][barcode][quantity][picture][flag][cat][tags]``

	[id] is just an arbitrary id number
	[name] is the name of the product
	[description] is the product description
	[barcode] is the barcode
	[quantity] is the current quantity
	[picture] storage of the main picture name
	[flag] is also reserved but can be manually set as it's just H,M or L for high priority, medium priority, and low priority, in terms of the quantity left. This will be used for shopping list generation later on when thats added to the API.
	[cat] the category
	[tags] a JSON array of tags

Product use is stored in a second MySQL table: `usage`
``[barcode][quantity][date]``

	[barcode] is the product barcode
	[quantity] is the products new quantity at the time the entry was added (after a change has happened to the quantity)
	[date] name says it all
	
Product stats are stored in a third table: `stats`
``[barcode][last_5][all]``

	[barcode] product barcode
	[last_5] rolling list of the last 5 standard rates which have been calculated
	[all] the total list of the standard rates which have been calculated

`pepper` contains the user and the OAuth:
``[user][passwd][secret][shared][data]``

		
	[user] The user's name
	[passwd] The users password, currently stored in plain text since user auth isn't implimented yet
	[secret] The users OAuth Secert key, if they have one.
	[shared] The users OAuth shared key, if they have one.
	[data] A JSON object containing info about the ip, time last logged in, and if the user is logged in.
		Sort of like a session, just a lot more barbaric.

`salt` is the same as `pepper` and currently is not used yet (haven't had the time).
`salt` is for backing up a deleted user, much like the backup database.

Other info:
-----------------

The API takes care of updating a product, searching and returning information about a product, returning the whole database for a total inventory, returning the usage log of the product, and stats on the product (only the linear regression of the data is available right now).
All returned data is in JSON format, and all queries should be by the barcode even though some types can take either name or barcode.

It is assumed you know how to install the Python libraries needed, place the Python scripts on a web server with 
Python and mod_wsgi and web.py and MySQL installed, along with run Python scripts and work SL4A.

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

Examples and testing scripts also use:

* poster
* urllib2