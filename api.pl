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
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/screen.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/print.css',-media=>'print'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'css/Aristo/jquery-ui-1.8.7.custom.css',-media=>'screen, projection'}),
	Link({-rel=>'stylesheet',-type=>'text/css',-href=>'http://code.jquery.com/mobile/1.0a3/jquery.mobile-1.0a3.min.css',-media=>'handheld'}));

my $jquery = <<END;
//setup jQuery so it doesn't cache the API calls
\$.ajaxSetup ({
	cache: false
});

//When the view button on the total inventory table is pressed, switch tabs and pull the JSON from the API
function doCommand(com, grid) {
	if (com == 'View') {
		\$('.trSelected', grid).each(function() {
			var id = \$('td:nth-child(1) div', this).html();
			\$("#search").val(id);
			//click the search button, this is a bit of a cheat that saves code
			\$("#load_basic").click();
		})
	}
};

\$(function() {
	//setup the tabs
	\$('#tabs').tabs();
	
	//setup the accordion inside the tabs
	\$('#accordion').accordion({
		autoHeight: false
	});
	
	//setup the total inventory table and flexigrid
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
			{name: 'View', onpress : doCommand}
		],
		dataType: 'json',
		usepager: true,
		singleSelect: true,
		title: 'Total Inventory',
		useRp: true,
		rp: 15
	});
	
	//fill the total inventory table with the total inventory from the API
	var total;
	\$.get(loadUrl, {'type_of_query': 'total_inventory'},
		function(data){
		//you have to parse the JSON and turn it into JSON that flexigrid can read
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
	
	//parse the names and barcode from the API and then auto complete the search field with the data
	var tags;
	\$.get(loadUrl, {'type_of_query': "names"},
		function(data){
		tags = \$.parseJSON(data);
		\$("#search").autocomplete({
			source: tags
		});
	});
	
	//setup the editable fields for changing the database
	\$('#name.editableText, #barcode.editableText, #quantity.editableText, #description.editableText,  #flag.editableText').editableText();
	
	\$('.editableText').change(function(){
		var newValue = \$(this).html();
	});
	
	//setup the auto update for the total inventory tab so it updates every second to make sure it has all the products
	//and make sure the search bar is always updated
	function update() {
	
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
		
		setTimeout(update, 5000);
	};
	update();
	
	//setup the dialog for deleting a product
	\$('#dialog_delete').dialog({
		autoOpen: false,
		width: 600,
		buttons: {
			"Delete": function() {
				delete_product();
				\$(this).dialog("close"); 
			}, 
			"Cancel": function() { 
				\$(this).dialog("close"); 
			} 
		},
		modal: true
	});
	
	\$('#dialog_edit').dialog({
		autoOpen: false,
		width: 600,
		buttons: {
			"Edit": function() {
				edit_product();
				\$(this).dialog("close"); 
			}, 
			"Cancel": function() { 
				\$(this).dialog("close"); 
			} 
		},
		modal: true
	});
	
	\$('#dialog_add').dialog({
		autoOpen: false,
		width: 600,
		buttons: {
			"Add": function() {
				add_product();
				\$(this).dialog("close"); 
			}, 
			"Cancel": function() { 
				\$(this).dialog("close"); 
			} 
		},
		modal: true
	});
	
});

//select the search text in the search bar if it's clicked
\$("#search").click(function(){
	\$(this).select();
});

\$("#name_new").click(function(){
	\$(this).select();
});
\$("#barcode_new").click(function(){
	\$(this).select();
});
\$("#quantity_new").click(function(){
	\$(this).select();
});
\$("#flag_new").click(function(){
	\$(this).select();
});
\$("#description_new").click(function(){
	\$(this).select();
});

//if the find button has been pressed, get and set all the info for the fields and what not
var loadUrl = "api.pl";
\$("#load_basic").click(function(){
	\$( "#tabs" ).tabs( "select", 0 );
	\$('#update').hide();
	var query = \$("#search").val()
	\$.get(loadUrl, {'type_of_query': "product_info", 'query': query },
		function(data){
			//parse the JSON into javascript objects
			var results = \$.parseJSON(data);
			//set all the fields to the correct value from the JSON string
			\$("#name").html(results.name);
			\$("#barcode").html(results.barcode);
			\$("#quantity").html(results.quantity);
			\$("#description").html(results.description);
			\$("#flag").html(results.flag)
			if (results.flag == 'M') {
				if (\$("#flag").hasClass('error')) {
					\$("#flag").removeClass('error');
				};
				if (\$("#flag").hasClass('success')) {
					\$("#flag").removeClass('success');
				};
				\$("#flag").addClass('notice');
			} else if (results.flag == 'H') {
				if (\$("#flag").hasClass('notice')) {
					\$("#flag").removeClass('notice');
				};
				if (\$("#flag").hasClass('success')) {
					\$("#flag").removeClass('success');
				};
				\$("#flag").addClass('error');
			} else if (results.flag == 'L') {
				if (\$("#flag").hasClass('error')) {
					\$("#flag").removeClass('error');
				};
				if (\$("#flag").hasClass('notice')) {
					\$("#flag").removeClass('notice');
				};
				\$("#flag").addClass('success');
			};
			\$('#hide').show();
			//plot the two graphs
			var dataP;
			var query = \$("#barcode").html();
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
	\$('#dialog_edit').dialog('open');
});

function edit_product() {
	var name = \$("#name").html();
	var barcode = \$("#barcode").html();
	var quantity = \$("#quantity").html();
	var description = \$("#description").html();
	var flag = \$("#flag").html();
	\$.get(loadUrl, {'type_of_query': 'update_product','name': name, 'description': description, 'query': barcode, 'quantity':quantity, 'flag': flag},
		function(data){
			if (\$("#update").hasClass('notice')) {
				\$("#update").removeClass('notice');
			};
			\$('#update').html('Product Updated').addClass('success');
			\$('#update').show();
		}
	);
};

\$("#add").click(function(){
	\$('#dialog_add').dialog('open');
});

function add_product() {
	var name = \$("#name_new").val();
	var barcode = \$("#barcode_new").val();
	var quantity = \$("#quantity_new").val();
	var description = \$("#description_new").val();
	var flag = \$("#flag_new").val();
	\$.get(loadUrl, {'type_of_query': 'add_product','name': name, 'description': description, 'query': barcode, 'quantity':quantity, 'flag': flag},
		function(data){
			if (\$("#add").hasClass('notice')) {
				\$("#add").removeClass('notice');
			};
			\$('#add').html('Product Added!').addClass('success');
			\$('#add').show();
		}
	);
};

\$("#delete").click(function(){
	\$('#dialog_delete').dialog('open');
});

function delete_product() {
	var name = \$("#name").html();
	var barcode = \$("#barcode").html();
	var quantity = \$("#quantity").html();
	var description = \$("#description").html();
	var flag = \$("#flag").html();
	\$.get(loadUrl, {'type_of_query': 'remove_product','query': barcode},
		function(data){
			if (\$("#update").hasClass('success')) {
				\$("#update").removeClass('success');
			};
			\$('#update').html('Product Deleted').addClass('notice');
			\$('#update').show();
			\$("#hide").hide();
		}
	);
};
END

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
								$form->p({-id=>'barcode',-class=>"functions large editableText"},
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