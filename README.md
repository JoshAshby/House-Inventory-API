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

This branch of the API uses web.py, MySQL and mod_wsgi instead of Perl for the API, however the client and the web interface 
will remain the same across all branches (however the code base will have to change due to url scheme changes (hasn't happened yet due to API work)).

This branch may also intergrate R as the main statistics generation for the products. (It does but it doesn't, because rpy2 doesn't like to run in a web.py session,
and makes the program hang without any errors...) as a result, This branch includes a copy of linear.py (known as ashmath.py in this branch), my own Vector math type for Python which is used for the
linear math done in the stats function.

API Info:
--------------
Coming soon after this Python branch of the API is finished.

	/ General home page currently, It will eventually be the web front address... I think

The following return JSON formated data:

	/product/dog987/info/ Info for the product whos barcode comes after the /product/
	/product/dog987/delete/ Delete said product with barcode stated
	/product/add/ Add the given product according to the data in the POST sent to this url.
	/product/update/ Update the given product according to the data in the POST sent to this url. Min needed in the POST is barcode
	/product/ get the total products
	/product/names/ only the names and barcodes of all the products for auto complete
	/product/dog987/log/ display the quantity change log for the product
	/product/dog987/stats/ returns the predicted time of when the current stock will run out.

``/product/add/`` and ``/product/update/`` Both take POST requests only, unlike the rest of the functions which only take GET requests.
As a result, ``/product/add/`` takes the ``[barcode][name][description][quantity]`` and optionally, a ``[picture]`` file to be uploaded and linked to the product.

One can use the Python poster library to easily do this:

```python
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
register_openers()
datagen, headers = multipart_encode({"picture": open("add.png", "rb"), 'barcode': 'dog', 'name': 'god', 'description': 'dog', 'quantity': 5})
request = urllib2.Request("http://localhost/product/add/", datagen, headers)
print urllib2.urlopen(request).read()
```

``/product/update/`` takes a minimum of the products ``[barcode]``, but can optionally accept ``[name][description][newbarcode][quantity][picture]``

The following is what is typically returned from the API calls:

	/product/dog987/info/ {"picture": "dog987.png", "description": "A Dog", "barcode": "dog987", "name": "Beagle", "flag": "L", "quantity": 3, "id": 23}
	/product/dog987/delete/ {"picture": "dog.png", "description": "a dog of god", "deleted": "true", "barcode": "dog", "name": "god's dog", "flag": "L", "quantity": 8, "id": 52}
	/product/add/ {"picture": "dog.png", "added": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "quantity": 5, "id": 53}
	/product/update/ {"picture": "dog.png", "updated": "true", "description": "dog", "barcode": "dog", "name": "god", "flag": "L", "oldbarcode": "dog", "quantity": 3, "id": 53}
	/product/ [{"picture": "718103025027.png", "description": "Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.", "barcode": "718103025027", "name": "Green Graph Composition", "flag": "M", "quantity": 1, "id": 3}, {"picture": "3037921120217.png", "description": "Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.", "barcode": "3037921120217", "name": "Orange Graph Notebook", "flag": "L", "quantity": 1, "id": 4}]
	/product/names/ [{"barcode": "718103025027", "name": "Green Graph Composition"}, {"barcode": "3037921120217", "name": "Orange Graph Notebook"}, {"barcode": "043396366268", "name": "the social network"}, {"barcode": "dog987", "name": "Beagle"}]
	/product/dog987/log/ [["2011-03-19 01:15:17", 1], ["2011-02-19 01:15:09", 2], ["2011-02-06 00:47:43", 6], ["2011-02-05 00:47:43", 3]]
	/product/dog987/stats/ {"current": -28.0, "guess": -0.07142857142857142, "predictedNF": -28, "predicted": -28.0, "standard": -0.07142857142857142}

Note that the reponses for ``[/product/add/][/product/update/][/product/delete/]`` returns an additional JSON object stating that the product has been updated, deleted or added.
``[/product/add/]`` may also return with ``{"COP": "dog"}`` should a copy of that products barcode already exsist in the table. in this example, '``dog`` is the barcode of the product that there is a copy of.
Valid responses are ``[NED][NULL][NS][COP]`` ``[NED]`` meaning that there is Not Enough Data, ``[NULL]`` being maiinly for the picture and thumbnail group indicating no picture or thumbnail is available, and ``[NS]`` being for Nothing Submitted, `[COP]`` meaning Copy Of Product meaning that a copy of that products barcode already exsists in the table.

All pictures can be accessed at either ``/pictures/barcode.fileextension`` or ``/thumb/barcode_thumb.fileextension``

Database Info:
--------------------------

Products are stored in a MySQL database with the following columns:
``[id][name][description][barcode][quantity][picture][thumb][flag]``

	[id] is just an arbitrary id number
	[name] is the name of the product
	[description] is the product description
	[barcode] is the barcode
	[quantity] is the current quantity
	[picture] storage of the main picture name
	[thumb] Storage of the thumbnail name
	[flag] is also reserved but can be manually set as it's just H,M or L for high priority, medium priority, and low priority, in terms of the quantity left. This will be used for shopping list generation later on when thats added to the API.

Product use is stored in a second MySQL table which is formated like so:
``[barcode][quantity][date]``

	[barcode] is the product barcode
	[quantity] is the products new quantity at the time the entry was added (after a change has happened to the quantity)
	[date] name says it all
	
Product stats are stored in a third table:
``[barcode][last_5][all]``

	[barcode] product barcode
	[last_5] rolling list of the last 5 standard rates which have been calculated
	[all] the total list of the standard rates which have been calculated
	
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
* linear.py (aka: ashmath.py)
* ashpic.py
* PIL (Python Image Library)

Examples and testing scripts also use:

* poster
* urllib2