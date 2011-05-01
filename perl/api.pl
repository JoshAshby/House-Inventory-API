#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

use warnings;
use strict;
use CGI qw/:standard :html3/;
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

print $form->header();

my @css = (
        Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/flexigrid/flexigrid.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/editableText.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet/less',-type=>'text/css',-href=>'css/style.less',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/screen.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/print.css',-media=>'print'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/Aristo/jquery-ui-1.8.7.custom.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.css',-media=>'handheld'}));

do 'request.pl';
our $jquery;
	
if ($gui eq 'y') {
	print $form->start_html(-head=>\@css,
						-title=>'House Inventory API',
						-script=>[{-type=>'text/javascript', -src=>'javascript/less.js'},
							{-type=>'text/javascript',-src=>'https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'},
							{-type=>'text/javascript', -src=>'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/jquery-ui.min.js'},
							{-type=>'text/javascript',-src=>'javascript/jquery.flot.min.js'},
							{-type=>'text/javascript',-src=>'javascript/flexigrid.js'},
							{-type=>'text/javascript',-src=>'javascript/jquery.editableText.js'}
							]);
	print $form->div({-class=>'container ui-widget'},
		#setup the dialogs for the various functions.
		#These are divs but jquery makes them hidden, using them only as place holders in a way for the dialog
		$form->div({-id=>'dialog_delete', -title=>'Delete Product?'},
			$form->p({}, 'Are you sure you want to delete this product?')
		),
		$form->div({-id=>'dialog_add', -title=>'Add Product?'},
			$form->p({}, 'Are you sure you want to add this product?')
		),
		$form->div({-id=>'dialog_edit', -title=>'Edit Product?'},
			$form->p({}, 'Are you sure you want to submit the changes to this product?')
		),
		#start the main form, what you see
		$form->div({-class=>'span-24'},
			$form->h1("House Inventory API Webfront"),
			$form->h2("Please enter the name or barcode of a product you would like to look at:"),
			$form->p('Enter this info in the Search field, and press the Find button to search for that product'),
		),
		$form->div({-class=>'span-24', -id=>'tabs'},
		$form->ul(
			$form->li($form->a({-href=>'#tabs-1'}, 'Info' )),
			$form->li($form->a({-href=>'#tabs-2'}, 'Add Product' )),
			$form->li($form->a({-href=>'#tabs-3'}, 'Total Inventory' )),
			$form->li(
				$form->textfield(-id=>'search',-class=>"functions", -value=>'Search'), $form->button(-value=>"Find", -id=>"load_basic",-class=>"functions")
				)
			),
		$form->div({-id=>'tabs-1', -class=>'functions'},
			$form->div({},
				$form->p({-id=>'update',-class=>"functions"},
					''
				),
				$form->table({-id=>'hide',-style=>"display: none",-cellspacing=>10},
					Tr({},
						td({-width=>300},
							$form->div({},
								$form->p({-id=>'name',-class=>"functions large editableText"},
									''
								),
								$form->p({-id=>'barcode',-class=>"functions med editableText"},
									''
								),
								$form->p({-class=>"functions"},
									['Quantity: ',
									$form->div({-id=>'quantity', -class=>'editableText'}, '')]
								),
								$form->p({-class=>"functions"},
									['Flag: ',
									$form->div({-id=>'flag', -class=>'editableText'}, '')]
								),
								$form->p({-id=>'description',-class=>"functions editableText"},
									''
								)
							)
						),
						td({-width=>10},
						
						),
						td({-width=>540},
							$form->div({-id=>'accordion'},
								$form->h3($form->a({-href=>'#'}, 'Product Use Plot' )),
								$form->div($form->div({-id=>'statplotarea'},'')),
								$form->h3($form->a({-href=>'#'}, 'Product Stats' )),
								$form->div({-id=>'statarea'},''),
								$form->h3($form->a({-href=>'#'}, 'Product Operations' )),
								$form->div({},
									$form->button(-value=>"Update Product", -id=>"edit",-class=>"functions"),
									$form->button(-value=>"Delete Product", -id=>"delete",-class=>"functions")
								)
							)
						)
					)
				)
			)
		),
		$form->div({-id=>'tabs-2', -class=>'functions'},
			$form->div({-id=>'return'},
				$form->label({}, 'Name'),
				$form->textfield(-id=>'name_new',-class=>"functions", -value=>'Name'),
				$form->label({}, 'Barcode'),
				$form->textfield(-id=>'barcode_new',-class=>"functions", -value=>'Barcode'),
				$form->label({}, 'Quantity'),
				$form->textfield(-id=>'quantity_new',-class=>"functions", -value=>'Quantity'),
				$form->label({}, 'Flag'),
				$form->textfield(-id=>'flag_new',-class=>"functions", -value=>'Flag'),
				$form->label({}, 'Description'),
				$form->textarea(-id=>'description_new',-class=>"functions", -value=>'Description'),
				$form->button(-value=>"Add Product", -id=>"add",-class=>"functions")
			)
		),
		$form->div({-id=>'tabs-3', -class=>'functions'},
			$form->div({-id=>'total'},
				$form->table({-class=>'flex2'},
					tbody({},
						Tr({},
							td({},
								''
							)
						)
					)
				)
			)
		)
		)
	);
	print $form->script($jquery);
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
	} elsif ($type_of_query eq 'return_log') {
		print $inventory->return_log($query_value);
	} elsif ($type_of_query eq 'gen_stat') {
		print $inventory->gen_stats($query_value);
	} elsif ($type_of_query eq 'names') {
		print $inventory->names();
	} elsif ($type_of_query eq 'return_log_flot') {
		print $inventory->return_log_flot($query_value);
	} elsif ($type_of_query eq 'return_stat_flot') {
		print $inventory->return_stats_flot($query_value);
	} elsif ($type_of_query eq 'gen_stat_flot') {
		print $inventory->gen_stats_flot($query_value);
	}
}