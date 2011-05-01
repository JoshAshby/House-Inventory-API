use warnings;
use strict;

our $jquery = <<END;
//setup jQuery so it doesn't cache the API calls
\$.ajaxSetup ({
	cache: false
});

//When the view button on the total inventory table is pressed, switch tabs and pull the JSON from the API
function doCommand(com, grid) {
	if (com == 'View') {
		\$('.trSelected', grid).each(
			function() {
				var id = \$('td:nth-child(1) div', this).html();
				\$('#search').val(id);
				//click the search button, this is a bit of a cheat that saves code
				\$('#load_basic').click();
			}
		)
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
			{
				display: 'Name',
				name : 'name',
				width : 130,
				sortable : true,
				align: 'left'
			},
			{
				display: 'Barcode',
				name : 'barcode',
				width : 130,
				sortable : true,
				align: 'left'
			},
			{
				display: 'Quantity',
				name : 'quantity',
				width : 130,
				sortable : true,
				align: 'left'
			},
			{
				display: 'Flag',
				name : 'flag',
				width : 130,
				sortable : true,
				align: 'left'},
			{
				display: 'Description',
				name : 'description',
				width : 300,
				sortable : true,
				align: 'left'
			}
		],
		buttons : [
			{
				name: 'View',
				onpress : doCommand
			}
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
	//get the API's JSON reply
	\$.get(loadUrl, {'type_of_query': 'total_inventory'},
		function(data){
			//you have to parse the JSON and turn it into JSON that flexigrid can read
			total =\$.parseJSON(data);
			var po = [];
			//format the data into the correct format
			for (var i = 0; i <= total.length-1; i++) {
				po.push({cell: [total[i]['name'], total[i]['barcode'], total[i]['quantity'], total[i]['flag'], total[i]['description']]});
			};
			//place it all in a new JSON object the flexigrid can read
			var da = {
				total: total.length,
				page: 1,
				rows: po
			};
			//add the data to the table
			\$('.flex2').flexAddData(eval(da));
		}
	);
	
	//parse the names and barcode from the API and then auto complete the search field with the data
	var tags;
	//get the API's JSON reply
	\$.get(loadUrl, {'type_of_query': "names"},
		function(data){
			//parse the JSON in to javascript types
			tags =\$.parseJSON(data);
			//set the search field to auto complete with the tags
			\$('#search').autocomplete({
				source: tags
			});
		}
	);
	
	//setup the editable fields for changing the database
	\$('#name.editableText, #barcode.editableText, #quantity.editableText, #description.editableText,  #flag.editableText').editableText();
	
	//if the text has been changed, make sure it's updated when it is saved
	\$('.editableText').change(
		function(){
			var newValue = \$(this).html();
		}
	);
	
	//setup the auto update for the total inventory tab so it updates every second to make sure it has all the products
	//and make sure the search bar is always updated
	function update() {
		//get the API's JSON reply
		\$.get(loadUrl, {'type_of_query': 'total_inventory'},
			function(data){
				//parse the API's JSON into javascript types
				total = \$.parseJSON(data);
				var po = [];
				//make each cell unit in the proper format for flexigrid
				for (var i = 0; i <= total.length-1; i++) {
					po.push({cell: [total[i]['name'], total[i]['barcode'], total[i]['quantity'], total[i]['flag'], total[i]['description']]});
				};
				//format the flexigrid readable JSON
				var da = {
					total: total.length,
					page: 1,
					rows: po
				};
				//add the JSON data to the table
				\$('.flex2').flexAddData(eval(da));
			}
		);
		
		//get the new tags, if any, and then set the search field to auto complete with the new tags
		var tags;
		//get the API's JSON reply
		\$.get(loadUrl, {'type_of_query': "names"},
			function(data){
				//parse the API's JSON into javascript types
				tags = \$.parseJSON(data);
				//set the search field to auto complete with the new tags
				\$('#search').autocomplete({
					source: tags
				});
			}
		);

		//set the time out to 5 seconds, this is the refresh rate
		setTimeout(update, 5000);
	};
	
	//and call the function so everything keeps updating
	update();
});

//select the text fields so that if any are clicked, all the text is selected
\$('#search').click(
	function(){
		\$(this).select();
	}
);
\$('#name_new').click(
	function(){
		\$(this).select();
	}
);
\$('#barcode_new').click(
	function(){
		\$(this).select();
	}
);
\$('#quantity_new').click(
	function(){
		\$(this).select();
	}
);
\$('#flag_new').click(
	function(){
		\$(this).select();
	}
);
\$('#description_new').click(
	function(){
		\$(this).select();
	}
);

//if the find button has been pressed, get and set all the info for the fields and what not
var loadUrl = 'api.pl';
\$('#load_basic').click(
	function(){
		//switch to the info tab
		\$('#tabs').tabs('select', 0);
		//if the update field is showing, hide it since we have not done anything yet
		\$('#update').hide();
		//get the barcode or name from the search field
		var query = \$('#search').val()
		//and get the API's JSON reply for that product
		\$.get(loadUrl, {'type_of_query': "product_info", 'query': query },
			function(data){
				//parse the JSON into javascript objects
				var results = \$.parseJSON(data);
				//set all the fields to the correct value from the JSON string
				\$('#name').html(results.name);
				\$('#barcode').html(results.barcode);
				\$('#quantity').html(results.quantity);
				\$('#description').html(results.description);
				\$('#flag').html(results.flag)
				//then make sure the flag box is the correct color for the flag
				if (results.flag == 'M') {
					if (\$('#flag').hasClass('error')) {
						\$('#flag').removeClass('error');
					};
					if (\$('#flag').hasClass('success')) {
						\$('#flag').removeClass('success');
					};
					\$('#flag').addClass('notice');
				} else if (results.flag == 'H') {
					if (\$('#flag').hasClass('notice')) {
						\$('#flag').removeClass('notice');
					};
					if (\$('#flag').hasClass('success')) {
						\$('#flag').removeClass('success');
					};
					\$('#flag').addClass('error');
				} else if (results.flag == 'L') {
					if (\$('#flag').hasClass('error')) {
						\$('#flag').removeClass('error');
					};
					if (\$('#flag').hasClass('notice')) {
						\$('#flag').removeClass('notice');
					};
					\$('#flag').addClass('success');
				};
				//show the table and graph area
				\$('#hide').show();
				//plot the two graphs
				var dataP;
				//get the barcode of the product
				var query = \$('#barcode').html();
				//get the API's JSON reply for the product for the stats points
				\$.get(loadUrl, {'type_of_query': 'return_stat_flot', 'query': query},
					function(data){
						//parse the JSON
						dataP = \$.parseJSON(data);
						//setup the plot area for flot
						\$('#statplotarea').css('height', '250px');
						\$('#statplotarea').css('width', '540px');
						//now go get the line variables
						\$.get(loadUrl, {'type_of_query': 'gen_stat_flot', 'query': query},
							function(data){
								//parse the JSON
								var dataline = \$.parseJSON(data);
								var fit_line = [];
								//generate the line
								for (var i = dataP[dataP.length-1][0]; i <=dataP[0][0]; i += 1) {
									fit_line.push([i, (dataline[1]*i+dataline[0])]);
								};
								//plot everything with the right options
								\$.plot(\$('#statplotarea'),
									[
										{	
											data: dataP,
											label: 'Stats Points',
											legend: {
												show: true,
												margin: 10,
												backgroundOpacity: 0.5
											},points: {
												show: true,
												radius: 3
											}
										},
										{
											data: fit_line,
											label: 'Stats Fit Line',
											legend: {
												show: true,
												margin: 10,
												backgroundOpacity: 0.5
											}, lines: {
												show: true
											}
										}
									]
								);
							}
						);
					}
				);
			}
		);
	}
);

//if the edit button is pressed, pull up the edit dialog
\$('#edit').click(
	function(){
		\$('#dialog_edit').dialog('open');
	}
);

\$(function() {
	//setup the dialog for editing a product
	\$('#dialog_edit').dialog({
		autoOpen: false,
		width: 600,
		buttons: {
			'Edit': function() {
				edit_product();
				\$(this).dialog('close'); 
			}, 
			'Cancel': function() { 
				\$(this).dialog('close'); 
			} 
		},
		modal: true
	});
});

//if you are sure you want to edit it, update the database
function edit_product() {
	var name = \$('#name').html();
	var barcode = \$('#barcode').html();
	var quantity = \$('#quantity').html();
	var description = \$('#description').html();
	var flag = \$('#flag').html();
	\$.get(loadUrl, {'type_of_query': 'update_product','name': name, 'description': description, 'query': barcode, 'quantity':quantity, 'flag': flag},
		function(data){
			if (\$('#update').hasClass('notice')) {
				\$('#update').removeClass('notice');
			};
			\$('#update').html('Product Updated').addClass('success');
			\$('#update').show();
		}
	);
};

\$('#add').click(function(){
	\$('#dialog_add').dialog('open');
});

\$(function() {
	//setup the dialog for adding a product
	\$('#dialog_add').dialog({
		autoOpen: false,
		width: 600,
		buttons: {
			'Add': function() {
				add_product();
				\$(this).dialog('close'); 
			}, 
			'Cancel': function() { 
				\$(this).dialog('close'); 
			} 
		},
		modal: true
	});
});

//if you are sure you want to add it, update the database
function add_product() {
	var name = \$('#name_new').val();
	var barcode = \$('#barcode_new').val();
	var quantity = \$('#quantity_new').val();
	var description = \$('#description_new').val();
	var flag = \$('#flag_new').val();
	\$.get(loadUrl, {'type_of_query': 'add_product','name': name, 'description': description, 'query': barcode, 'quantity':quantity, 'flag': flag},
		function(data){
			if (\$('#add').hasClass('notice')) {
				\$('#add').removeClass('notice');
			};
			\$('#add').html('Product Added!').addClass('success');
			\$('#add').show();
		}
	);
};

\$('#delete').click(function(){
	\$('#dialog_delete').dialog('open');
});

\$(function() {
	//setup the dialog for deleting a product
	\$('#dialog_delete').dialog({
		autoOpen: false,
		width: 600,
		buttons: {
			'Delete': function() {
				delete_product();
				\$(this).dialog('close'); 
			}, 
			'Cancel': function() { 
				\$(this).dialog('close'); 
			} 
		},
		modal: true
	});
});

//if you are sure you want to delete it, update the database
function delete_product() {
	var name = \$('#name').html();
	var barcode = \$('#barcode').html();
	var quantity = \$('#quantity').html();
	var description = \$('#description').html();
	var flag = \$('#flag').html();
	\$.get(loadUrl, {'type_of_query': 'remove_product','query': barcode},
		function(data){
			if (\$('#update').hasClass('success')) {
				\$('#update').removeClass('success');
			};
			\$('#update').html('Product Deleted').addClass('notice');
			\$('#update').show();
			\$('#hide').hide();
		}
	);
};
END

