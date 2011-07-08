spam = 0
	
$.ajaxSetup
	cache: false

base = '../'
	
nut = base + 'product/'
	
fredrick = {
	'picture': ( base + 'picture/')
	'thumb': ( base + 'thumb/')
	'add': ( nut + 'add/')
	'update': ( nut + 'update/')
	'delete': '/delete/'
	'log': '/log/'
	'info': '/info/'
	'stats': '/stats/'
}
		
update = ->
	$.getJSON nut, (data) ->
		if data
			$('#total').show()
			$('#total_error').hide()
			$('#total').html ''
			(if i%2 == 0
				b = 'shade'
			else
				b = ''
			$('#total').append "<tr class='pro #{ b }'><td><img src='#{ fredrick['thumb'] + data[i]['picture'] }' alt='#{ data[i]['picture'] }' width='64px'/></td><td>#{ data[i]['barcode'] }</td><td>#{ data[i]['name'] }</td><td>#{ data[i]['quantity'] }</td><td><span id='toolbar'><span id='action#{ data[i]['barcode'] }'><input type='radio' id='info#{ data[i]['barcode'] }' name='action#{ data[i]['barcode'] }' checked='checked' /><label for='info#{ data[i]['barcode'] }'>Info</label><input type='radio' id='delete#{ data[i]['barcode'] }' name='action#{ data[i]['barcode'] }' /><label for='delete#{ data[i]['barcode'] }'>Delete</label></span><button id='punch_it#{ data[i]['barcode'] }' bar='#{ data[i]['barcode'] }'>Do it!</button></span></td></tr>"
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
		else
			$("#total").hide()
			$('#total_error').show()
		
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
	$('#info').show()
	$('#tabs').tabs 'select',  1
	$.getJSON nut + secret_mess + fredrick['info'], (data) ->
		$('#name_info').html data['name']
		$('#update_name').attr 'value', data['name']
		$('#barcode_info').html data['barcode']
		$('#update_barcode_old').attr 'value', data['barcode']
		$('#quantity_info').html data['quantity']
		$('#update_quantity').attr 'value', data['quantity']
		$('#description_info').html data['description']
		$('#update_description').attr 'value', data['description']
		$('#picture_info').html "<img src='#{ fredrick['thumb'] + data['picture'] }' alt='#{ data['picture'] }' width='128px'/>"
		$('#large_picture_info').html "<img src='#{ fredrick['picture'] + data['picture'] }' alt='#{ data['picture'] }' width='100%'/>"
	$.getJSON nut + secret_mess + fredrick['stats'], (data) ->
		$('#stat_info').html data['predicted']
		$('#rank_info').html data['rank']
		$('#pop_info').html data['popularity']
	$.getJSON nut + secret_mess + fredrick['log'], (data) ->
		$('#log_info').html ''
		for elk in [0..data.length-1]
			if elk%2 == 0
				b = 'shade'
			else
				b = ''
			egg = data[elk].toString()
			yeast= data[elk].filter -> 
				raptop = egg.match /(.*(?!^)(:..))/
				zygot = egg.match /([0-9]+)/
				return [raptop,zygot]
			$('#log_info').append "<tr class='pro #{ b }'><td>#{ yeast[0] }</td><td>#{ yeast[1] }</td></tr>"
			
troll = ->
	barcode = $('#barcode').val()
	$('#old').html barcode
	$('#dialog_add').dialog 'open'

check = ->
	val = $('#picture').val()
	if val
		$('#picTrue').val '1'
	else
		$('#picTrue').val '0'
	setTimeout check, 100
	
			
$ ->
	$('#info').hide()
	$('#update_form').hide()

	$( "#accordion_info" ).accordion {
		autoHeight: false
	}

	$( "#accordion_help" ).accordion {
		autoHeight: false
	}

	$('#tabs').tabs()
	update()

	$('#dialog_del').dialog {
		autoOpen: false
		width: 600
		buttons: {
			'On second thought...':  c
			'TRASH IT NOW!': a
		}
		modal: true
	}

	$('#dialog_add').dialog {
		autoOpen: false
		width: 600
		buttons: {
			'Rock On!': c
		}
		modal: true
	}
		
	$('#enter_if_you_dare').button().click ->
		troll()
	
	$('#you_entered_didnt_you').button().click ->
		$(this).hide()
		$('#update_form').show()
		
		$('#name_info').edit('init')
		$('#barcode_info').edit('init')
		$('#quantity_info').edit('init')
		$('#description_info').edit('init')
	
	$('#you_entered_didnt_you_submit').button().click ->
		$('#update_form').hide()
		$('#you_entered_didnt_you').show()
		
		$('#name_info').edit('destroy')
		$('#barcode_info').edit('destroy')
		$('#quantity_info').edit('destroy')
		$('#description_info').edit('destroy')
		
		setTimeout update, 1000
	
	$('#barcode_info').focusout ->
		val = $('#barcode_info').html()
		$('#update_form').append "<input type='hidden' name='newbarcode' id='update_barcode' value='#{ val }'/>"
	$('#name_info').focusout ->
		val = $('#name_info').html()
		$('#update_form').append  "<input type='hidden' name='name' id='update_name' value='#{ val }'/>"
	$('#quantity_info').focusout ->
		val = $('#quantity_info').html()
		$('#update_form').append  "<input type='hidden' name='quantity' id='update_quantity' value='#{ val }'/>"
	$('#description_info').focusout ->
		val = $('#description_info').html()
		$('#update_form').append  "<input type='hidden' name='description' id='update_description' value='#{ val }'/>"
	check()