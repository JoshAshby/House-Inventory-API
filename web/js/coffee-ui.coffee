	spam = 0
	
	$.ajaxSetup
		cache: false
	
	base = 'http://localhost/'
	
	nut = base + 'product/'
	
	fredrick = {
		'picture': ( base + 'picture/'),
		'thumb': ( base + 'thumb/'),
		'add': ( nut + 'add/'),
		'update': ( nut + 'update/'),
		'delete': '/delete/',
		'log': '/log/',
		'info': '/info/',
		'stats': '/stats/'
	}
		
	update = ->
		$.getJSON nut, (data) ->
			$('#total').html ''
			(if i%2 == 0
				b = 'shade'
			else
				b = ''
			$('#total').append '<tr id="total_pro" class="' + b + '"><td><img src="' + fredrick['thumb'] + data[i]['picture']+ '" alt="' + data[i]['picture'] + '" width="64px"/></td><td>' + data[i]['barcode'] + '</td><td>' + data[i]['name'] + '</td><td>' + data[i]['quantity'] + '</td><td><span id="toolbar"><span id="action' + data[i]['barcode'] + '"><input type="radio" id="info' + data[i]['barcode'] + '" name="action' + data[i]['barcode'] + '" checked="checked" /><label for="info' + data[i]['barcode'] + '">Info</label><input type="radio" id="delete' + data[i]['barcode'] + '" name="action' + data[i]['barcode'] + '" /><label for="delete' + data[i]['barcode'] + '">Delete</label></span><button id="punch_it' + data[i]['barcode'] + '" bar=' +  data[i]['barcode'] + '>Do it!</button></span></td></tr>' 
			$('#punch_it' + data[i]['barcode']).button().click ->
				goo = $(this).attr 'bar'
				if $("label[for='info#{goo}']").attr('aria-pressed') == 'true'
					e(goo)
				else
					$('#yeller').html goo
					$('#dialog_del').dialog 'open'
			$('#action' + data[i]['barcode']).buttonset()) for i in [0..data.length-1]
			if spam
				setTimeout update, 5000
			
	a = ->
		bar_soap = $('#yeller').html()
		$.get nut + bar_soap + fredrick['delete'], (data) ->
			update()
		$(this).dialog 'close'
	
	c = ->
		$(this).dialog 'close'
		update()
		$('#barcode').val ''
		$('#name').val ''
		$('#description').val ''
		$('#quantity').val ''
		$('#picture').val ''
		$('#tabs').tabs 'select',  0
	
	e = (secret_mess) ->
		$('#tabs').tabs 'select',  1
		$('#tabs-2').html ''
		$.getJSON nut + secret_mess + fredrick['info'], (data) ->
			$('#tabs-2').append "<h2 class='bold_fancy'>#{ data['name'] }</h2><p>Click on a field to edit it then press submit</p><table id='clean'><tr><td>Barcode:</td><td>#{ data['barcode']} </td></tr><tr class='small'><td width='200px'>Quantity:</td><td>#{ data['quantity'] }</td></tr><tr height='20px'></tr><tr><td colspan='3'>#{ data['description'] }</td></tr></table>"
	
	troll = ->
		barcode = $('#barcode').val()
		$('#old').html barcode
		$('#dialog_add').dialog 'open'
				
	$ ->
		$('#tabs').tabs()
		$('#tabs-1').html '<table><h3 class="bold_fancy">Total Stock</h3><p>Click on either Do it! or change the seletion to delete toview the info or delete a product</p><thead><tr id="total_pro"><th>Picture</th><th>Barcode</th><th>Name</th><th>Quantity</th><th>Action</th></tr></thead><tbody id="total"></tbody></table>'
		update()
		$('#dialog_del').dialog {
			autoOpen: false
			width: 600
			buttons: {
				'Delete': a
				'Cancel':  c
			}
			modal: true
		}
		$('#dialog_add').dialog {
			autoOpen: false
			width: 600
			buttons: {
				'Great!': c
			}
			modal: true
		}
			
		$('#enter_if_you_dare').button().click ->
			troll()
			