House Inventory API
===================

Simple API written in Perl which handles all the nasty stuff for keeping a basic inventory.
Products are stored in a MySQL database with the following columns:
``[id][name][description][barcode][quantity]``

The API takes care of updating a product by either name or barcode (adding or removing a product or quantity), searching and returning information about a product which can be by either name or barcode, and returning the whole database.
All returned data is in JSON format.


This next section assumes you, the user, knows how to deploy a simple Perl script and install the needed CPAN packages.
Needed packages are:
CGI
DBI/DBD::mysql
JSON
(You can install them from CPAN)


To use simply make sure you have a MySQL database which matches, modify the settings in database.pl to fit your server, and then start sending POST or GET requests in a format like so: ``/index.pl?type_of_query=______&query=__________``
where ``_____`` is replaced by the correct query type and query.House Inventory API
===================

Simple API written in Perl which handles all the nasty stuff for keeping a basic inventory.
Products are stored in a MySQL database with the following columns:
``[id][name][description][barcode][quantity]``

The API takes care of updating a product by either name or barcode (adding or removing a product or quantity), searching and returning information about a product which can be by either name or barcode, and returning the whole database.
All returned data is in JSON format.


This next section assumes you, the user, knows how to deploy a simple Perl script and install the needed CPAN packages.
Needed packages are:
CGI
DBI/DBD::mysql
JSON
(You can install them from CPAN)


To use simply make sure you have a MySQL database which matches, modify the settings in database.pl to fit your server, and then start sending POST or GET requests in a format like so: ``/index.pl?type_of_query=______&query=__________``
where ``_____`` is replaced by the correct query type and query.

type_of_query currently include ``total_inventory`` ``single_product_info`` ``update_product``
and query can be either a barcode, or a name of a product, capitalization does not matter.

Included is also a Python script to test the API. It will send a POST request with the two system arguments to the API and print the returned data. To use it: ``python request.py barcode 123456789`` or ``python request.py name Pineapple``

type_of_query currently include ``total_inventory`` ``single_product_info`` ``update_product``
and query can be either a barcode, or a name of a product, capitalization does not matter.

Included is also a Python script to test the API. It will send a POST request with the two system arguments to the API and print the returned data. To use it: ``python request.py barcode 123456789`` or ``python request.py name Pineapple``
