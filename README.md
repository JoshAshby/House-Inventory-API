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
DBI\DBD::mysql
JSON
(You can install them from CPAN)

More for this file on use and install, along with more general info to come later when it's done.
