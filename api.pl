#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

use warnings;
use strict;

use CGI;
use database;

my $form=new CGI;
my $type_of_query=CGI::escapeHTML($form->param("type_of_query"));
my $query_value=CGI::escapeHTML($form->param("query"));
my $description_value=CGI::escapeHTML($form->param("description"));
my $name_value=CGI::escapeHTML($form->param("name"));
my $quantity_value=CGI::escapeHTML($form->param("quantity"));
my $flag_value=CGI::escapeHTML($form->param("flag"));

my $inventory = database->new();

print $form->header();

if ($type_of_query eq 'single_product_info') {
	$inventory->print_info($query_value);
} elsif ($type_of_query eq 'total_inventory') {
	$inventory->total_inventory();
} elsif ($type_of_query eq 'update_product_quantity') {
	$inventory->update_product_quantity($query_value, $quantity_value);
} elsif ($type_of_query eq 'add_new_product') {
	$inventory->add_product($name_value, $description_value, $query_value, $quantity_value, $flag_value);
} elsif ($type_of_query eq 'update_product_info') {
	$inventory->update_product_info($name_value, $description_value, $query_value, $quantity_value);
} elsif ($type_of_query eq 'remove_product') {
	$inventory->delete_product($query_value);
} elsif ($type_of_query eq 'return_stat') {
	$inventory->return_log($query_value);
}