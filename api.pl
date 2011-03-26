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
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/screen.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/print.css',-media=>'print'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/Aristo/jquery-ui-1.8.7.custom.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.css',-media=>'handheld'}));

my @names = $inventory->names();

my $jquery = <<END;
\$.ajaxSetup ({
	cache: false
});

function doCommand(com, grid) {
	if (com == 'View') {
		\$('.trSelected', grid).each(function() {
			var id = \$('td:nth-child(1) div', this).html();
			\$("#search").val(id);
			\$("#load_basic").click();
			\$( "#tabs" ).tabs( "select", 0 );
		})
	}
};

\$(function() {
	\$('#tabs').tabs();
	\$('#accordion').accordion({
		autoHeight: false
	});
	var loadUrl = 'api.pl';
	\$('.flex2').flexigrid({
		colModel : [
			{display: 'Name', name : 'name', width : 130, sortable : true, align: 'left'},
			{display: 'Barcode', name : 'barcode', width : 130, sortable : true, align: 'left'},
			{display: 'Quantity', name : 'quantity', width : 130, sortable : true, align: 'left'},
			{display: 'Flag', name : 'flag', width : 130, sortable : true, align: 'left'},
			{display: 'Description', name : 'description', width : 300, sortable : true, align: 'left'}
		],
		buttons : [
			{name: 'View', bclass: 'view', onpress : doCommand}
		],
		dataType: 'json',
		usepager: true,
		singleSelect: true,
		title: 'Total Inventory',
		useRp: true,
		rp: 15
	});
	var loadUrl = "api.pl";
	var total;
	\$.get(loadUrl, {'type_of_query': 'total_inventory'},
		function(data){
		total = \$.parseJSON(data);
		var po = [];
		for (var i = 0; i <= total.length-1; i++) {
			po.push({cell: [total[i]['name'], total[i]['barcode'], total[i]['quantity'], total[i]['flag'], total[i]['description']]});
		};
		var da = {
		total: total.length,
		page: 1,
		rows: po
		};
		\$(".flex2").flexAddData(eval(da));
	});

	var tags;
	\$.get(loadUrl, {'type_of_query': "names"},
		function(data){
		tags = \$.parseJSON(data);
		\$("#search").autocomplete({
			source: tags
		});
	});
});

\$("#search").click(function(){
	\$("#search").select();
});

var loadUrl = "api.pl";
\$("#load_basic").click(function(){
	var query = \$("#search").val()
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
			//plot the two graphs
			var dataP;
			var query = \$("#barcode").val();
			\$.get(loadUrl, {'type_of_query': "return_stat_flot", 'query': query},
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
					var statplotarea = \$("#statplotarea");
					statplotarea.css("height", "250px");
					statplotarea.css("width", "540px");
					\$.get(loadUrl, {'type_of_query': "gen_stat_flot", 'query': query},
						function(data){
							var dataline = \$.parseJSON(data);
							var fit_line = [];
							for (var i = dataP[dataP.length-1][0]; i <=dataP[0][0]; i += 1) {
								fit_line.push([i, (dataline[1]*i+dataline[0])]);
							};
							var options_line = {
								legend: {
									show: true,
									margin: 10,
									backgroundOpacity: 0.5
								},points: {
									show: true,
									radius: 3
								}, lines: {
									 show: true
								}
							};
							\$.plot(statplotarea, [{data: dataP, label: 'Stats Points', legend: {
									show: true,
									margin: 10,
									backgroundOpacity: 0.5
								},points: {
									show: true,
									radius: 3
								}}, {data: fit_line, label: 'Stats Fit Line', legend: {
									show: true,
									margin: 10,
									backgroundOpacity: 0.5
								}, lines: {
									 show: true
								}}]);
						});
				});
		});
});

\$("#edit").click(function(){
	var name = \$("#name").val();
	var barcode = \$("#barcode").val();
	var quantity = \$("#quantity").val();
	var description = \$("#description").val();
	var flag = \$("#flag").val();
	
});
END

if ($gui eq 'y') {
	print $form->start_html(-head=>\@css,
						-title=>'House Inventory API',
						-script=>[{-type=>'text/javascript', -src=>'javascript/less.js'},
							{-type=>'text/javascript',-src=>'https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js'},
							{-type=>'text/javascript', -src=>'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/jquery-ui.min.js'},
							{-type=>'text/javascript', -src=>'http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.js'},
							{-type=>'text/javascript',-src=>'javascript/jquery.flot.min.js'},
							{-type=>'text/javascript',-src=>'javascript/flexigrid.js'}
							]);
	print $form->div({-class=>'container ui-widget'},
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
			$form->div({-class=>''},
				$form->table({-width=>'100%'},
					tbody({},
						Tr({},
							th({-width=>'130'}, ['Name', 'Barcode']),
							th({-width=>'100%'}, ['plot'])
						),
						Tr({},
							td({},[
								$form->textarea(-id=>'name',-class=>"functions",-columns=>'20',-rows=>2),
								$form->textarea(-id=>'barcode',-class=>"functions",-columns=>'20',-rows=>2)
							]),
							td({-rowspan=>'7'},[
								$form->div({-id=>'accordion'},
									$form->h3($form->a({-href=>'#'}, 'Product Use Plot' )),
									$form->div($form->div({-id=>'statplotarea'},'')),
									$form->h3($form->a({-href=>'#'}, 'Product Stats' )),
									$form->div({-id=>'statarea'},'')
								)
							]),
						),
						Tr({},
							th({}, ['Quantity', 'Flag',])
						),
						Tr({},
							td({},[
								$form->textarea(-id=>'quantity',-class=>"functions",-columns=>'20',-rows=>2),
								$form->textarea(-id=>'flag',-class=>"functions",-columns=>'20',-rows=>2)
							])
						),
						Tr({},
							th({-colspan=>'2'}, ['Description'])
						),
						Tr({},
							td({-colspan=>'2'}, [
								$form->textarea(-id=>'description',-class=>"functions",-columns=>'45',-rows=>20)
							])
						)
						Tr({},
							td({-colspan=>'2'}, [
								$form->button(-value=>"Edit Product", -id=>"edit",-class=>"functions"),
								$form->button(-value=>"Delete Product", -id=>"delete",-class=>"functions"),
							])
						)
					)
				)
			)
		),
		$form->div({-id=>'tabs-2', -class=>'functions'},$form->div({-id=>'return'},'')),
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