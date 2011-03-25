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
	
my @css = (Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/style.less',-media=>'screen, projection'}),
        Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/screen.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/print.css',-media=>'print'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/Aristo/jquery-ui-1.8.7.custom.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.css',-media=>'handheld'}));

my @names = $inventory->names();
	
my $start = <<END;
\$(function() {
	\$( "#tabs" ).tabs();
});
END

my $jquery = <<END;
\$.ajaxSetup ({
	cache: false
});

\$(function() {
	var loadUrl = "api.pl";
	var tags;
	\$.get(loadUrl, {'type_of_query': "names"},
		function(data){
		tags = \$.parseJSON(data);
		\$("#query").autocomplete({
			source: tags
		});
	});
});

var loadUrl = "api.pl";
\$("#load_basic").click(function(){
	var query = \$("#query").val()
	\$.get(loadUrl, {'type_of_query': "product_info", 'query': query },
		function(data){
			//parse the JSON into javascript objects
			var results = \$.parseJSON(data);
			//set all the fields to the correct value from the JSON string
			\$("#name").val(results.name);
			\$("#barcode").val(results.barcode);
			\$("#quantity").val(results.quantity);
			\$("#description").val(results.description);
			\$("#flag").val(results.flag);
			//plot the two graphs (only one implemented so far)
			var dataP;
			var query = \$("#barcode").val();
			\$.get(loadUrl, {'type_of_query': "gen_stat_flot", 'query': query},
				function(data){
					dataP = \$.parseJSON(data);
					var options = {
						legend: {
							show: true,
							margin: 10,
							backgroundOpacity: 0.5
						},points: {
							show: true,
							radius: 3
						}
					};
					var useplotarea = \$("#useplotarea");
					useplotarea.css("height", "250px");
					useplotarea.css("width", "500px");
					\$.plot(useplotarea, [{data: dataP, label: 'Stats Points'}], options);
					});
		});
});
END
	
if ($gui eq 'y') {
	print $form->start_html(-head=>\@css,
						-title=>'House Inventory API',
						-script=>[{-type=>'text/javascript', -src=>'javascript/less.js'},
							{-type=>'text/javascript',-src=>'https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'},
							{-type=>'text/javascript', -src=>'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/jquery-ui.min.js'},
							{-type=>'text/javascript', -src=>'http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.js'},
							{-type=>'text/javascript',-src=>'javascript/jquery.flot.min.js'}]);
	print $form->script($start);
	print $form->div({-class=>'container ui-widget'},
		$form->div({-class=>'span-24'},
			$form->h1("House Inventory API Webfront"),
			$form->h2("Please enter the name or barcode of a product you would like to look at:"),
			$form->textfield(-id=>'query',-class=>"functions"),
			$form->button(-value=>"Find", -id=>"load_basic",-class=>"functions"),
			$form->hr()),
		$form->div({-class=>'span-8'},
			$form->table({-border=>undef},
				Tr({-align=>'CENTER',-valign=>'TOP'},
					[th([$form->label('Name'),$form->textfield(-id=>'name',-class=>"functions")]),
					td([$form->label('Barcode'),$form->textfield(-id=>'barcode',-class=>"functions")]),
					td([$form->label('Quantity'),$form->textfield(-id=>'quantity',-class=>"functions")]),
					td([$form->label('Description'),$form->textarea(-id=>'description',-class=>"functions",-columns=>30,-rows=>10)]),
					td([$form->label('Flag'),$form->textfield(-id=>'flag',-class=>"functions")])
					]))
		),
		$form->div({-class=>'span-16 last', -id=>'tabs'},
		$form->ul(
			$form->li($form->a({-href=>'#tabs-1'}, 'Product Use Plot' )),
			$form->li($form->a({-href=>'#tabs-2'}, 'Product Stats Plot' )),
			$form->li($form->a({-href=>'#tabs-3'}, 'Result' )),
			$form->li($form->a({-href=>'#tabs-4'}, 'Return' ))
		),
		$form->div({-id=>'tabs-1'},$form->div({-id=>'statsplotarea'},'Plot area')),
		$form->div({-id=>'tabs-2'},$form->div({-id=>'useplotarea'},'Plot area')),
		$form->div({-id=>'tabs-3', -class=>'functions'},$form->p({-id=>'results'},'Some results')),
		$form->div({-id=>'tabs-4', -class=>'functions'},$form->p({-id=>'return'},'Some returns'))
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
	} elsif ($type_of_query eq 'gen_stat_flot') {
		print $inventory->return_stats_flot($query_value);
	}
}