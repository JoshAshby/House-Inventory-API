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
my $gui = CGI::escapeHTML($form->param("gui"));

my $inventory = database->new();

#need to clean this all up for CGI but thats for tomorrow...
#also, please note that the base UI will be built and tested and working before the GUI elements (jQuery, Less.js, flot.js and bluetrip)
#are intergrated. These declarations are simply so they are here for when I do get the UI finished (shouldn't take that long)

#Less.js will get used most likely, just a matter of figuring out what I want to change in bluetrip and want to do it easily with Less.js
my $css = "<!--<script src=\"/javascript/less.js\"></script>-->
<link rel=\"stylesheet/less\" type=\"text/css\" href=\"/css/style.less\ media=\"screen, projection\">
<link rel=\"stylesheet\" href=\"/css/screen.css\" type=\"text/css\" media=\"screen, projection\">
<link rel=\"stylesheet\" href=\"/css/print.css\" type=\"text/css\" media=\"print\">
<!--[if IE]>
	<link rel=\"stylesheet\" href=\"/css/ie.css\" type=\"text/css\" media=\"screen, projection\">
<![endif]-->";
#Plain vanilla jQuery
my $jquery = "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js\"></script>";
#jQuery UI for normal interface
my $jquery_ui = "<script src=\"https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/jquery-ui.min.js\"></script>
<link type=\"text/css\" href=\"/css/Aristo/jquery-ui-1.8.7.custom.css\" rel=\"stylesheet\"/>";
#jQuery Mobile for mobile interfaces (or all interfaces depending on what I decide)
my $jquery_mobile = "<link rel=\"stylesheet\" href=\"http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.css\" />
<script src=\"http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.js\"></script>";
#and finally Flot for the graphs
my $flot = "<!--[if lte IE 8]><script language=\"javascript\" type=\"text/javascript\" src=\"/javascript/excanvas.min.js\"></script><![endif]-->
<script language=\"javascript\" type=\"text/javascript\" src=\"/javascript/jquery.flot.min.js\"></script>";

print $form->header();

if ($gui eq 'y') {
	#code for the web front goes here
	print $form->start_html(-title=>'House Inventory API');
	print $form->end_html();
} else {
	if ($type_of_query eq 'product_info') {
		print $inventory->print_info($query_value);
	} elsif ($type_of_query eq 'total_inventory') {
		print $inventory->total_inventory();
	} elsif ($type_of_query eq 'add_product') {
		print $inventory->add_product($name_value, $description_value, $query_value, $quantity_value, $flag_value);
	} elsif ($type_of_query eq 'update_product') {
		print $inventory->update_product($name_value, $description_value, $query_value, $quantity_value, $flag_value);
	} elsif ($type_of_query eq 'remove_product') {
		print $inventory->delete_product($query_value);
	} elsif ($type_of_query eq 'return_stat') {
		print $inventory->return_log($query_value);
	}
}